import altair as alt
import pandas as pd
import numpy as np
import streamlit as st


alt.data_transformers.disable_max_rows(); 

st.set_page_config(
    layout="wide",
	initial_sidebar_state = "auto", 
	page_title = "HPV dashboard",
    page_icon = 'img/hpv.png'
)

@st.cache_data
def load_data():
    df = pd.read_csv('/Users/akitakeiko/visualization_BMI706/Data/combined_dfall.csv', index_col = 0)
    return df

df = load_data()
st.write("## Temporal HPV cases and cohort sizes by Countries")
year = st.slider("Year", min_value=2010, max_value=2030, value=2021)
subset = df[df["year"] == year]


countries_default = [
    "Austria",
    "United Kingdom",
    "Brazil",
    "Spain",
    "China",
    "United States",
    "Iceland",
]
countries_df =  df["country_name"].unique()
countries = st.multiselect("Countries", options = countries_df, default = countries_default)
subset = subset[subset["country_name"].isin(countries)]

income_df = df["income_group"].unique()
income = st.selectbox("Income Group", options=income_df, index=income_df.tolist().index("Low income"))
subset = subset[subset["income_group"] == income]


