import streamlit as st
import pandas as pd
from engine.risk import QUESTIONS, score_answers
from engine.allocation import recommend, rebalance_plan, weights_from_amounts
from engine.compliance import DISCLAIMER
from engine.data_sources import load_holdings_csv

st.set_page_config(page_title="WealthGPT Starter", page_icon="💹")

st.title("WealthGPT Starter 💹")
st.caption("Educational prototype – not investment advice.")

with st.sidebar:
    st.header("Investor Profile")
    age = st.number_input("Age", min_value=18, max_value=90, value=40, step=1)
    years_to_goal = st.number_input("Years to primary goal", min_value=0, max_value=60, value=10, step=1)
    st.markdown("---")
    st.subheader("Risk Profiler")
    answers = []
    for i,(q, opts) in enumerate(QUESTIONS):
        choice = st.selectbox(q, list(opts.keys()), key=f"q{i}")
        answers.append(choice)
    risk = score_answers(answers)
    st.info(f"Risk score: {risk.score} → **{risk.label}**")
    st.markdown("---")
    uploaded = st.file_uploader("Upload your holdings CSV (asset_class,instrument,amount)", type=["csv"])

st.subheader("Current Portfolio")
if uploaded:
    df = load_holdings_csv(uploaded)
else:
    st.caption("Using sample data (upload to replace).")
    df = pd.read_csv("example_data/holdings_sample.csv")
st.dataframe(df)

corpus = float(df["amount"].sum())
current_weights = df.groupby("asset_class")["amount"].sum()
current_weights = (current_weights / current_weights.sum()).to_dict()

st.subheader("Recommended Allocation")
rec = recommend(risk.label, age, years_to_goal if years_to_goal>0 else None)
rec_df = pd.DataFrame({
    "Asset Class": list(rec.split.keys()),
    "Target %": [round(v*100,1) for v in rec.split.values()],
    "Current %": [round(current_weights.get(k,0)*100,1) for k in rec.split.keys()],
})
st.dataframe(rec_df)

st.subheader("Rebalance Plan")
plan = rebalance_plan(current_weights, rec.split, corpus)
plan_df = pd.DataFrame({"Asset Class": plan.keys(), "Buy(+)/Sell(-) ₹": plan.values()})
st.dataframe(plan_df)

csv = plan_df.to_csv(index=False).encode("utf-8")
st.download_button("Download Rebalance CSV", data=csv, file_name="rebalance_plan.csv", mime="text/csv")

st.markdown("---")
st.caption(DISCLAIMER)
