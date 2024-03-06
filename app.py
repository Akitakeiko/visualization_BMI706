import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import os


from data_clean import combined_df
df = combined_df()


## Streamlit configurations
st.set_page_config(
    layout="wide",
	initial_sidebar_state = "auto", 
	page_title = "HPV dashboard",
    page_icon = 'img/hpv.png'
)

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

nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['year'], empty='none')

# Task 3
bar_current_cov = alt.Chart(df).mark_bar().encode(
    y='year:O',  # Year on the y-axis
    x='current_cov:Q',  # Current coverage values on the x-axis
    color=alt.value('steelblue')  # Bar color
).properties(
    title='Current Coverage by Year'
)

# Create the horizontal bar chart for curr_cost
bar_curr_cost = alt.Chart(df).mark_bar().encode(
    y='year:O',  # Year on the y-axis
    x='curr_cost:Q',  # Current cost values on the x-axis
    color=alt.value('firebrick')  # Bar color
).properties(
    title='Current Cost by Year'
)

# Use Streamlit to display the charts
st.write("## Current Coverage by Year")
st.altair_chart(bar_current_cov, use_container_width=True)
st.write("## Current Cost by Year")
st.altair_chart(bar_curr_cost, use_container_width=True)