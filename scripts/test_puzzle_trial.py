"""Tests for scripts/puzzle_trial.py. Run: python3 -m unittest scripts/test_puzzle_trial.py"""
import copy
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import puzzle_trial as pt  # noqa: E402


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.base = pt.load()
        self.tmp = Path(tempfile.mkdtemp()) / "m.json"
        pt.save(copy.deepcopy(self.base), self.tmp)

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = pt.main(list(args) + ["--manifest", str(self.tmp)])
        return code, out.getvalue(), err.getvalue()

    def data(self):
        return json.loads(self.tmp.read_text())

    def test_current_candidates_pass(self):
        code, out, _ = self.run_cli("check")
        self.assertEqual(code, 0, out)

    def test_duplicate_design_refused(self):
        code, _, err = self.run_cli("record", "--id", "P21-02-v1", "--event", "design_created",
                                    "--design-id", "DAXXXXXXXXX")
        self.assertEqual(code, 1)
        self.assertIn("duplicate", err)
        self.assertEqual(pt.find(self.data(), "P21-02-v1")["canva"]["design_id"], "DAHYt_HUDes")

    def test_plan_without_design_searches_before_copying(self):
        d = self.data()
        c = pt.find(d, "P21-03-v1")
        c["canva"]["design_id"] = None
        c["canva"]["state"] = None
        steps = pt.plan_for(c)
        self.assertIn("search Canva", steps[0])
        self.assertIn("copy", steps[1])

    def test_stale_approval_after_wording_change(self):
        code, _, _ = self.run_cli("approve", "--id", "P21-02-v1", "--kind", "content", "--by", "Hoang")
        self.assertEqual(code, 0)
        d = self.data()
        c = pt.find(d, "P21-02-v1")
        self.assertEqual(pt.approval_status(c)["content"], "valid")
        c["slides"]["question"]["prompt"] += " Think carefully."
        self.assertEqual(pt.approval_status(c)["content"], "STALE")

    def test_visual_change_also_stales(self):
        self.run_cli("approve", "--id", "P21-03-v1", "--kind", "design", "--by", "Hoang")
        c = pt.find(self.data(), "P21-03-v1")
        c["visual_spec_version"] = "2"
        self.assertEqual(pt.approval_status(c)["design"], "STALE")

    def test_missing_assumption_blocks(self):
        c = pt.find(self.data(), "P21-02-v1")
        c["slides"]["question"]["assumptions"].remove("The printer and packer can work at the same time.")
        errs = pt.check_candidate(c)
        self.assertTrue(any("work at the same time" in e for e in errs), errs)
        self.assertIn("BLOCKED", pt.plan_for(c)[0])

    def test_answer_leak_blocks(self):
        c = pt.find(self.data(), "P21-03-v1")
        c["slides"]["question"]["visual_text"].append("Hint: Ben. gives up ¼")
        errs = pt.check_candidate(c)
        self.assertTrue(any("answer leak" in e for e in errs), errs)

    def test_wrong_maths_detected(self):
        c = pt.find(self.data(), "P21-02-v1")
        c["maths"]["jobs"]["A"] = [2, 8]
        self.assertTrue(pt.check_maths(c))

    def test_failed_export_keeps_export_in_plan(self):
        self.run_cli("record", "--id", "P21-02-v1", "--event", "edits_committed")
        self.run_cli("record", "--id", "P21-02-v1", "--event", "export_failed", "--note", "timeout")
        c = pt.find(self.data(), "P21-02-v1")
        self.assertEqual(c["exports"][-1]["status"], "failed")
        self.assertTrue(any("export PNG" in s for s in pt.plan_for(c)))

    def test_uncertain_write_blocks_until_inspected(self):
        self.run_cli("record", "--id", "P21-02-v1", "--event", "write_uncertain", "--note", "commit timed out")
        code, _, err = self.run_cli("record", "--id", "P21-02-v1", "--event", "edits_committed")
        self.assertEqual(code, 1)
        self.assertIn("uncertain", err)
        c = pt.find(self.data(), "P21-02-v1")
        self.assertIn("BLOCKED", pt.plan_for(c)[0])
        code, _, _ = self.run_cli("record", "--id", "P21-02-v1", "--event", "inspected",
                                  "--note", "state=saved; design shows committed edits")
        self.assertEqual(code, 0)
        self.assertEqual(pt.find(self.data(), "P21-02-v1")["canva"]["state"], "saved")

    def test_publish_approval_refused_in_trial(self):
        code, _, err = self.run_cli("approve", "--id", "P21-02-v1", "--kind", "publish", "--by", "Hoang")
        self.assertEqual(code, 1)
        self.assertIn("disabled", err)

    def test_exactly_two_slides(self):
        c = pt.find(self.data(), "P21-02-v1")
        c["slides"]["bonus"] = {}
        self.assertTrue(any("exactly two slides" in e for e in pt.check_candidate(c)))


if __name__ == "__main__":
    unittest.main()
