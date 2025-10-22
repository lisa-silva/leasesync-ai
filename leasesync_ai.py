import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, timedelta

# Cool Cherrywood styling
st.set_page_config(page_title="LeaseSync AI", page_icon="📝", layout="wide")
st.markdown("<style>body {background-color: #E8F5E9; font-family: 'Arial', sans-serif;}</style>", unsafe_allow_html=True)

# Connect to database (fake for now)
conn = sqlite3.connect("leases.db")

# Sample lease data
@st.cache_data
def load_data():
    data = pd.DataFrame({
        "tenant_id": [1, 2, 3],
        "name": ["John Doe", "Jane Smith", "Bob Lee"],
        "lease_end": ["2026-01-15", "2025-11-30", "2025-12-20"],
        "rent": [2000, 1800, 2200],
        "status": ["Active", "Active", "Pending Renewal"]
    })
    return data

# Predict renewal likelihood (simple rule-based AI)
def predict_renewal(data):
    today = datetime.now()
    data["days_to_end"] = [(datetime.strptime(date, "%Y-%m-%d") - today).days for date in data["lease_end"]]
    data["renewal_chance"] = [80 if days < 60 else 50 for days in data["days_to_end"]]
    return data

# App
st.sidebar.image("https://via.placeholder.com/150?text=Cherrywood+Logo", width=150)  # Replace with real logo
st.sidebar.title("LeaseSync AI")
page = st.sidebar.selectbox("Pick a Page", ["Lease Overview", "Renewal Predictions", "Dashboard"])

data = load_data()

if page == "Lease Overview":
    st.header("Lease Management")
    st.table(data[["tenant_id", "name", "lease_end", "rent", "status"]])
    st.write("Upload new lease data (CSV):")
    uploaded_file = st.file_uploader("Choose file", type="csv")
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        st.table(new_data)

elif page == "Renewal Predictions":
    st.header("Renewal Predictions")
    data = predict_renewal(data)
    st.table(data[["tenant_id", "name", "lease_end", "renewal_chance"]])
    for index, row in data.iterrows():
        if row["renewal_chance"] > 60:
            st.success(f"Send renewal offer to {row['name']}!")
        else:
            st.warning(f"Follow up with {row['name']}.")

else:
    st.header("Lease Dashboard")
    fig = px.bar(data, x="name", y="rent", color="status", title="Rent by Tenant")
    st.plotly_chart(fig)
