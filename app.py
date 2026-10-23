import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.models import BudgetCredibilityAnalyzer

st.set_page_config(page_title="Kenya MTEF Budget Credibility Diagnostic", layout="wide")

analyzer = BudgetCredibilityAnalyzer()
fiscal_df = analyzer.load_fiscal_space()
revenue_df = analyzer.load_revenue_execution()
sector_df = analyzer.load_sector_ceilings()

st.title("Kenya National Treasury: MTEF Budget Credibility & Fiscal Space Tracker")
st.markdown(
    """
    **Practitioner Portfolio Deliverable | Public Finance Management (PFM)**  
    *Diagnostic analysis utilizing published Budget Policy Statements (BPS) and Public Sector Hearing datasets.*
    """
)

tab1, tab2, tab3 = st.tabs(["Fiscal Space & Rigid Claims", "Q1 Revenue Variance", "MTEF Ceilings"])

with tab1:
    st.subheader("Structural Fiscal Space Squeeze")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Shock Simulator")
        shock = st.slider("Consolidated Fund Services Shock (+% pts):", 0.0, 15.0, 2.5, 0.5)
        sim_df = analyzer.simulate_debt_shock(shock)
        latest_rigid = sim_df.iloc[-1]["stressed_rigid_pct"]
        latest_disc = sim_df.iloc[-1]["stressed_discretionary_pct"]
        
        st.metric("Projected Rigid Claims (FY26/27)", f"{latest_rigid:.1f}%")
        st.metric("Remaining Discretionary Space", f"{latest_disc:.1f}%")

    with col2:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(sim_df["fiscal_year"], sim_df["debt_service_pension_share_pct"], label="Baseline Rigid Claims (%)", color="#D9534F", marker="o")
        ax.plot(sim_df["fiscal_year"], sim_df["stressed_rigid_pct"], label="Simulated Stress Path", color="#A8201A", linestyle="--")
        ax.set_ylabel("Share of Ordinary Revenue (%)")
        ax.legend()
        st.pyplot(fig)

with tab2:
    st.subheader("Q1 Execution Realization Rate vs. Target")
    st.dataframe(
        revenue_df[["revenue_category", "target_bn", "actual_bn", "variance_bn", "execution_pct"]],
        use_container_width=True
    )

with tab3:
    st.subheader("Medium-Term Expenditure Ceilings Distribution")
    st.bar_chart(sector_df.set_index("sector")["share_2027_28_pct"])
