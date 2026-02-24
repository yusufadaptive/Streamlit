import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Adaptive & Co Ads Auditor", layout="wide")

st.title("🚀 Adaptive & Co | Google Ads Legend Dash")
st.write("Real-time audit of €5,450.41 Spend")

# Helper function to handle Google Ads CSV formatting
def load_data(filename):
    try:
        # skiprows=2 ignores the junk header rows from Google exports
        df = pd.read_csv(filename, skiprows=2)
        return df
    except Exception as e:
        st.error(f"Waiting for {filename}... Ensure it is uploaded to GitHub.")
        return None

# Sidebar for navigation
menu = st.sidebar.radio("Analysis Menu", ["Campaign Overview", "Search Term Auditor"])

if menu == "Campaign Overview":
    df = load_data("campaigns.csv")
    if df is not None:
        st.header("Campaign Performance")
        # Creating a quick chart of Cost vs Conversions
        fig = px.bar(df, x="Campaign", y="Cost", title="Spend by Campaign")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

elif menu == "Search Term Auditor":
    df_terms = load_data("search_terms.csv")
    if df_terms is not None:
        st.header("🔍 Search Term Auditor")
        
        # Logic to find "Wasted Spend" (Cost > 0 and 0 Conversions)
        waste = df_terms[(df_terms['Conversions'] == 0) & (df_terms['Cost'] > 5)]
        
        col1, col2 = st.columns(2)
        col1.metric("Wasted Search Terms", f"{len(waste)}")
        col2.metric("Potential Monthly Savings", f"€{waste['Cost'].sum():.2f}")
        
        st.subheader("High-Cost Terms to Add as Negatives")
        st.dataframe(waste[['Search term', 'Cost', 'Clicks']].sort_values(by='Cost', ascending=False))
