#!/usr/bin/env python3
"""
Generate branded chart PNGs for the weekly CMO report into docs/reports/assets/.

Charts are grounded in real research (the seasonal spine + the live TikTok hashtag scan), not
invented metrics. Update the data dicts here as real performance data arrives post-launch.
Run: python3 scripts/build_report_charts.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ASSETS = Path(__file__).resolve().parents[1] / "docs" / "reports" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

# Brand palette (config/brand.ts)
BLUE, ACCENT, EMERALD, MUTED, INK, PAPER = "#467DE3", "#60A5FA", "#10B981", "#94A3B8", "#020817", "#FFFFFF"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
    "axes.edgecolor": "#CBD5E1", "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "figure.facecolor": PAPER, "axes.facecolor": PAPER, "savefig.facecolor": PAPER,
})


def _clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def seasonal_demand():
    """Exam-season demand intensity across the launch window — the strategic spine."""
    months = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"]
    intensity = [0.10, 0.10, 0.22, 0.42, 0.92, 0.80, 0.88, 0.50]  # qualitative, from the EU autumn cycle
    x = range(len(months))

    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    ax.fill_between(x, intensity, color=BLUE, alpha=0.12)
    ax.plot(x, intensity, color=BLUE, linewidth=2.4, marker="o", markersize=5, markerfacecolor=BLUE)

    # build window shading (Jun-Aug)
    ax.axvspan(-0.3, 2.0, color=MUTED, alpha=0.12)
    ax.text(0.85, 0.16, "BUILD\n(plant content)", ha="center", va="center", fontsize=8.5,
            color="#475569", weight="bold")
    # launch marker
    ax.axvline(3, color=EMERALD, linestyle="--", linewidth=1.4)
    ax.text(3, 1.02, "Launch  Sep 1", ha="center", fontsize=8.5, color=EMERALD, weight="bold")
    # harvest annotations
    ax.annotate("Midterm spike", xy=(4, 0.92), xytext=(4.1, 0.62), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="->", color="#475569"))
    ax.annotate("Finals spike", xy=(6, 0.88), xytext=(6.05, 0.58), fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle="->", color="#475569"))

    ax.set_xticks(list(x)); ax.set_xticklabels(months)
    ax.set_yticks([]); ax.set_ylim(0, 1.12); ax.set_xlim(-0.3, 7.3)
    ax.set_title("When our buyer actually needs us  ·  EU autumn exam cycle",
                 fontsize=12.5, weight="bold", loc="left", pad=10)
    _clean(ax); ax.spines["left"].set_visible(False)
    fig.tight_layout()
    out = ASSETS / "seasonal-demand.png"
    fig.savefig(out, dpi=150); plt.close(fig)
    return out


def hashtag_landscape():
    """Live TikTok hashtag sizes — shows the open exact-concept lane (log scale)."""
    data = [  # (label, videos, is_target)
        ("#studytok", 4_200_000, False),
        ("#accounting", 376_000, False),
        ("#contabilidad", 354_000, False),
        ("#fintok", 161_100, False),
        ("#accountingstudent", 70_600, True),
        ("#businessschool", 43_900, False),
        ("#corporatefinance", 5_611, False),
        ("#financialaccounting", 4_036, True),
    ]
    data = data[::-1]  # smallest at top
    labels = [d[0] for d in data]
    vals = [d[1] for d in data]
    colors = [BLUE if d[2] else MUTED for d in data]

    fig, ax = plt.subplots(figsize=(8.4, 3.6))
    bars = ax.barh(labels, vals, color=colors, height=0.62)
    ax.set_xscale("log")
    ax.set_xlim(2_000, 8_000_000)

    def fmt(v):
        return f"{v/1_000_000:.1f}M" if v >= 1_000_000 else (f"{v/1000:.0f}K" if v >= 1000 else str(v))
    for b, v in zip(bars, vals):
        ax.text(v * 1.15, b.get_y() + b.get_height() / 2, fmt(v), va="center", fontsize=9, color=INK)

    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt(v)))
    ax.set_title("The exact-concept lane is wide open  ·  TikTok videos per hashtag (log scale)",
                 fontsize=12.5, weight="bold", loc="left", pad=10)
    ax.text(0.0, -0.22, "Blue = where our buyer is (and where we can win).  Grey = adjacent / wrong intent.",
            transform=ax.transAxes, fontsize=8.5, color="#475569")
    _clean(ax); ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    out = ASSETS / "hashtag-landscape.png"
    fig.savefig(out, dpi=150, bbox_inches="tight"); plt.close(fig)
    return out


if __name__ == "__main__":
    for fn in (seasonal_demand, hashtag_landscape):
        print("wrote", fn())
