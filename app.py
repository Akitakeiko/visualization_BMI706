import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    combined_df= pd.read_csv('https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/combined_dfall.csv?token=GHSAT0AAAAAACOCXHGSHQQGSCNSFILX42HUZPHZWIA', index_col = 0)
    return combined_df

df = load_data()

st.write("## Temporal HPV cases and cohort sizes by Countries")
year = st.slider("Year", min_value=2010, max_value=2030, value=2021)
subset = df[df["Year"] == year]
