from pathlib import Path
import pandas as pd
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def test_data_files_exist():
    for f in [
        "fiscal_space_trends.csv",
        "q1_revenue_execution.csv",
        "sector_ceilings_mtef.csv",
    ]:
        assert (DATA_DIR / f).exists(), f"Missing file: {f}"


def test_execution_percentage_bounds():
    df = pd.read_csv(DATA_DIR / "q1_revenue_execution.csv")
    assert (df["execution_pct"] > 0).all()
    assert (df["execution_pct"] < 300).all()


def test_sector_share_sum():
    df = pd.read_csv(DATA_DIR / "sector_ceilings_mtef.csv")
    assert pytest.approx(df["share_2027_28_pct"].sum(), rel=1e-2) == 100.0
