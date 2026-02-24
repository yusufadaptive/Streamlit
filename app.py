import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Adaptive & Co Ads Auditor", layout="wide")

st.title("🚀 Adaptive & Co | Google Ads Legend Dash")
st.write("Real-time audit of €5,450.41 Spend")

def load_data(filename):
    try:
        # We try skipping 2 rows first, then 3 if it fails
        for skip in [2, 3]:
            df = pd.read_csv(filename, skiprows=skip)
            df.columns = df.columns.str.strip()
            # If we find a numeric column, we've successfully hit the data
            if not df.select_dtypes(include=['number']).columns.empty:
                return df.dropna(how='all')
        return pd.read_csv(filename) # Fallback to raw
    except Exception:
        return None

menu = st.sidebar.radio("Analysis Menu", ["Campaign Overview", "Search Term Auditor"])

if menu == "Campaign Overview":
    df = load_data("campaigns.csv")
    if df is not None:
        st.header("Campaign Performance")
        
        # AUTO-DETECT COLUMNS: Finds first text column and first number column
        text_cols = df.select_dtypes(include=['object']).columns
        num_cols = df.select_dtypes(include=['number']).columns
        
        if not text_cols.empty and not num_cols.empty:
            fig = px.bar(df, x=text_cols[0], y=num_cols[0], title=f"Spend Breakdown by {text_cols[0]}")
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df)
    else:
        st.error("Waiting for campaigns.csv... ensure it is named correctly in GitHub.")

elif menu == "Search Term Auditor":
    df_terms = load_data("search_terms.csv")
    if df_terms is not None:
        st.header("🔍 Search Term Auditor")
        
        # Find numeric columns for Cost and Conversions dynamically
        num_cols = df_terms.select_dtypes(include=['number']).columns
        cost_col = [c for c in num_cols if 'Cost' in c] or [num_cols[0]]
        conv_col = [c for c in num_cols if 'Conv' in c] or [num_cols[-1]]
        
        # Calculate Waste: Cost > 5 and Conversions == 0
        waste = df_terms[(df_terms[conv_col[0]] == 0) & (df_terms[cost_col[0]] > 5)]
        
        c1, c2 = st.columns(2)
        c1.metric("Wasted Search Terms", len(waste))
        c2.metric("Potential Savings", f"€{waste[cost_col[0]].sum():.2f}")
        
        st.subheader("High-Cost Negative Keyword Targets")
        st.dataframe(waste.sort_values(by=cost_col[0], ascending=False))
