from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass(frozen=True)
class PFMPaths:
    """Centralized path management across operating systems."""

    base_dir: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = base_dir / "data"
    output_dir: Path = base_dir / "outputs"


class BudgetCredibilityAnalyzer:
    """Institutional fiscal analysis engine for National Treasury MTEF data."""

    def __init__(self, paths: PFMPaths = PFMPaths()):
        self.paths = paths
        self.paths.output_dir.mkdir(parents=True, exist_ok=True)

    def load_fiscal_space(self) -> pd.DataFrame:
        df = pd.read_csv(self.paths.data_dir / "fiscal_space_trends.csv")
        df["discretionary_space_pct"] = 100.0 - df["debt_service_pension_share_pct"]
        return df

    def load_revenue_execution(self) -> pd.DataFrame:
        df = pd.read_csv(self.paths.data_dir / "q1_revenue_execution.csv")
        df["variance_bn"] = df["actual_bn"] - df["target_bn"]
        df["execution_gap_pct"] = df["execution_pct"] - 100.0
        return df

    def load_sector_ceilings(self) -> pd.DataFrame:
        return pd.read_csv(self.paths.data_dir / "sector_ceilings_mtef.csv")

    def simulate_debt_shock(self, shock_percentage_points: float) -> pd.DataFrame:
        """Simulate the impact of an exogenous debt service spike on discretionary space."""
        df = self.load_fiscal_space().copy()
        df["stressed_rigid_pct"] = (
            df["debt_service_pension_share_pct"] + shock_percentage_points
        )
        df["stressed_discretionary_pct"] = 100.0 - df["stressed_rigid_pct"]
        return df
