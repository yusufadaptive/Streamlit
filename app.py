import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Adaptive & Co Ads Auditor", layout="wide")

st.title("🚀 Adaptive & Co | Google Ads Legend Dash")
st.write("Real-time audit of €5,450.41 Spend")

def load_data(filename):
    try:
        # Skips metadata and cleans up hidden spaces in headers
        df = pd.read_csv(filename, skiprows=2)
        df.columns = df.columns.str.strip() 
        # Remove total/summary rows that often appear at the bottom
        df = df[df.iloc[:, 0].notna()] 
        return df
    except Exception:
        st.error(f"Waiting for {filename}... Check GitHub filenames.")
        return None

menu = st.sidebar.radio("Analysis Menu", ["Campaign Overview", "Search Term Auditor"])

if menu == "Campaign Overview":
    df = load_data("campaigns.csv")
    if df is not None:
        st.header("Campaign Performance")
        
        # Flex-fix: Find columns that look like Campaign and Cost
        col_x = [c for c in df.columns if 'Campaign' in c][0]
        col_y = [c for c in df.columns if 'Cost' in c][0]
        
        fig = px.bar(df, x=col_x, y=col_y, title=f"Spend by {col_x}")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

elif menu == "Search Term Auditor":
    df_terms = load_data("search_terms.csv")
    if df_terms is not None:
        st.header("🔍 Search Term Auditor")
        
        # Standardizing column names for the logic
        df_terms.columns = [c.replace('Search term', 'Term').replace('Conversions', 'Conv') for c in df_terms.columns]
        
        # Logic: Find waste (No conversions and cost > 5)
        cost_col = [c for c in df_terms.columns if 'Cost' in c][0]
        conv_col = [c for c in df_terms.columns if 'Conv' in c][0]
        
        waste = df_terms[(df_terms[conv_col] == 0) & (df_terms[cost_col] > 5)]
        
        c1, c2 = st.columns(2)
        c1.metric("Wasted Search Terms", len(waste))
        c2.metric("Potential Savings", f"€{waste[cost_col].sum():.2f}")
        
        st.subheader("High-Cost Negative Keyword Targets")
        st.dataframe(waste.sort_values(by=cost_col, ascending=False))
