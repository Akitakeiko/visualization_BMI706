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
df_melted = df.melt(id_vars=['year'], value_vars=['proj_cost', 'curr_cost'], var_name='category', value_name='value')

# Create the stacked bar chart
stacked_bar_chart = alt.Chart(df_melted).mark_bar().encode(
    x='year:N',  # N indicates nominal/categorical data
    y=alt.Y('sum(value):Q', stack='zero', title='Total Value'),  # Stack the bars
    color='category:N',  # Differentiate by category
    tooltip=['year:N', 'category:N', 'sum(value):Q']
).properties(
    width=600,
    height=400,
    title='Yearly Comparison of Current and Projection Cost'
)

# Display the chart in the Streamlit app
st.write("# Yearly Comparison of Current and Projection Cost")
st.altair_chart(stacked_bar_chart, use_container_width=True)