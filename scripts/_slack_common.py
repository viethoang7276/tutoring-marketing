"""Shared Slack helpers: env loading (.env then .env.local, then real env) + a thin API call."""
import os, json
from pathlib import Path
import requests

REPO = Path(__file__).resolve().parents[1]
SLACK_API = "https://slack.com/api"


def load_env():
    env = {}
    for name in (".env", ".env.local"):  # .env.local overrides .env
        f = REPO / name
        if not f.exists():
            continue
        for raw in f.read_text(encoding="utf8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k, v in os.environ.items():  # real shell env wins
        if k.startswith("SLACK_") or k.startswith("CLAUDE_"):
            env[k] = v
    return env


def slack_api(method, token, json_body=None, data=None):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{SLACK_API}/{method}"
    if json_body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        r = requests.post(url, headers=headers, data=json.dumps(json_body), timeout=30)
    else:
        r = requests.post(url, headers=headers, data=data or {}, timeout=30)
    out = r.json()
    if not out.get("ok"):
        raise RuntimeError(f"Slack {method} failed: {out.get('error')} ({out})")
    return out
