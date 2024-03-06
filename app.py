import altair as alt
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data()
    mixed_df= pd.read_csv('https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/combined_dfall.csv?token=GHSAT0AAAAAACOCXHGS4LMCJZZR5KPR3TH6ZPHXDOQ', index_col = 0)
    return df

df = load_data()
st.write("## Age-specific cancer mortality rates")
