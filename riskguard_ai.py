import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px

st.set_page_config(page_title="RiskGuard AI", page_icon="⚠️", layout="wide")
st.markdown("<style>body {background-color: #FFF3E0; font-family: 'Arial', sans-serif;}</style>", unsafe_allow_html=True)

# Sample data
@st.cache_data
def load_data():
    data = pd.DataFrame({
        "weather": ["rainy", "sunny", "windy", "rainy"],
        "crew_size": [10, 15, 8, 12],
        "budget": [50000, 75000, 40000, 60000],
        "risk_level": [1, 0, 1, 1]  # 1=high risk
    })
    return data

# AI Model
def predict_risk(data):
    X = pd.get_dummies(data[["weather", "crew_size", "budget"]])
    y = data["risk_level"]
    model = RandomForestClassifier().fit(X, y)
    new_data = pd.DataFrame({
        "weather": ["windy"], "crew_size": [9], "budget": [45000]
    })
    X_new = pd.get_dummies(new_data).reindex(columns=X.columns, fill_value=0)
    risk = model.predict_proba(X_new)[0][1]
    return risk * 100

# App
st.sidebar.title("RiskGuard AI")
page = st.sidebar.selectbox("View", ["Risk Prediction", "Risk Trends"])

data = load_data()

if page == "Risk Prediction":
    st.header("Project Risk Prediction")
    risk_score = predict_risk(data)
    st.metric("High Risk Probability", f"{risk_score:.1f}%")
    if risk_score > 50:
        st.warning("Mitigate: Increase crew or check weather.")

else:
    st.header("Risk Dashboard")
    fig = px.bar(data, x="weather", y="risk_level", title="Risk by Factor")
    st.plotly_chart(fig)