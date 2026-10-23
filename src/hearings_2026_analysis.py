from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NAVY = "#0F2A4A"
TEAL = "#008080"
CORAL = "#D9534F"
SLATE = "#5C6B73"
LIGHT_BG = "#F9FBFD"

plt.rcParams.update(
    {
        "font.sans-serif": "DejaVu Sans",
        "font.family": "sans-serif",
        "figure.facecolor": LIGHT_BG,
        "axes.facecolor": LIGHT_BG,
        "axes.edgecolor": SLATE,
        "axes.grid": True,
        "grid.color": "#E5E5E5",
        "grid.linestyle": "--",
    }
)


def generate_fiscal_space_chart() -> Path:
    df = pd.read_csv(DATA_DIR / "fiscal_space_trends.csv")
    fig, ax1 = plt.subplots(figsize=(10, 5.5))
    ax1.plot(
        df["fiscal_year"],
        df["debt_service_pension_share_pct"],
        color=CORAL,
        marker="o",
        linewidth=2.5,
    )
    ax1.set_ylabel("Rigid Claims (%)", color=CORAL, fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=CORAL)
    ax1.set_ylim(10, 60)
    for _, row in df.iterrows():
        ax1.annotate(
            f"{row['debt_service_pension_share_pct']}%",
            (row["fiscal_year"], row["debt_service_pension_share_pct"] + 1.5),
            ha="center",
            fontsize=9,
            color=CORAL,
        )
    ax2 = ax1.twinx()
    ax2.plot(
        df["fiscal_year"],
        df["ordinary_revenue_gdp_pct"],
        color=NAVY,
        marker="s",
        linewidth=2.5,
        linestyle="--",
    )
    ax2.set_ylabel("Revenue (% of GDP)", color=NAVY, fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=NAVY)
    ax2.set_ylim(10, 25)
    ax2.grid(False)
    for _, row in df.iterrows():
        ax2.annotate(
            f"{row['ordinary_revenue_gdp_pct']}%",
            (row["fiscal_year"], row["ordinary_revenue_gdp_pct"] - 1.5),
            ha="center",
            fontsize=9,
            color=NAVY,
        )
    plt.title(
        "Kenya Fiscal Space Squeeze (FY2013/14 – FY2026/27)",
        fontsize=13,
        fontweight="bold",
        pad=16,
        color=NAVY,
    )
    fig.tight_layout()
    target = OUTPUT_DIR / "fiscal_space_chart.png"
    plt.savefig(target, dpi=300)
    plt.close()
    return target


def generate_revenue_execution_chart() -> Path:
    df = pd.read_csv(DATA_DIR / "q1_revenue_execution.csv").sort_values(
        by="execution_pct", ascending=True
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_colors = [
        CORAL if val < 90 else (TEAL if val >= 100 else NAVY)
        for val in df["execution_pct"]
    ]
    bars = ax.barh(
        df["revenue_category"], df["execution_pct"], color=bar_colors, height=0.6
    )
    ax.axvline(100, color="gray", linestyle=":", linewidth=1.5)
    ax.set_xlabel("Execution Rate (%)", fontsize=11, fontweight="bold")
    ax.set_xlim(0, 130)
    for bar in bars:
        w = bar.get_width()
        ax.annotate(
            f"{w:.1f}%",
            xy=(w + 1.5, bar.get_y() + bar.get_height() / 2),
            va="center",
            fontsize=9,
            fontweight="bold",
        )
    plt.title(
        "Q1 Budget Execution Rate by Revenue Category",
        fontsize=13,
        fontweight="bold",
        pad=16,
        color=NAVY,
    )
    fig.tight_layout()
    target = OUTPUT_DIR / "q1_revenue_execution_chart.png"
    plt.savefig(target, dpi=300)
    plt.close()
    return target


def generate_sector_ceilings_chart() -> Path:
    df = pd.read_csv(DATA_DIR / "sector_ceilings_mtef.csv").sort_values(
        by="share_2027_28_pct", ascending=False
    )
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.bar(df["sector"], df["share_2027_28_pct"], color=TEAL, width=0.55)
    ax.set_ylabel("Share of Ceilings (%)", fontsize=11, fontweight="bold")
    for _, row in df.iterrows():
        ax.annotate(
            f"{row['share_2027_28_pct']}%\n(Δ+{row['growth_to_2030_pct']}%)",
            xy=(row["sector"], row["share_2027_28_pct"] + 0.8),
            ha="center",
            fontsize=8.5,
        )
    ax.set_ylim(0, 50)
    plt.title(
        "MTEF Sector Ceilings (FY2027/28) & Growth to 2030",
        fontsize=13,
        fontweight="bold",
        pad=16,
        color=NAVY,
    )
    plt.xticks(rotation=20, ha="right")
    fig.tight_layout()
    target = OUTPUT_DIR / "sector_ceilings_chart.png"
    plt.savefig(target, dpi=300)
    plt.close()
    return target


def main():
    generate_fiscal_space_chart()
    generate_revenue_execution_chart()
    generate_sector_ceilings_chart()
    print("Execution complete. Visualizations written to outputs/")


if __name__ == "__main__":
    main()
