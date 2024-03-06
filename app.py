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
                        fields=['Year'], empty='none')

# The basic line
line_cov = alt.Chart(data).mark_bar().encode(
    x='Year:O',
    y='current_cov:Q',
    color=alt.value('steelblue')  # Bar color
).add_selection(
    nearest
)

line_cost = alt.Chart(data).mark_bar().encode(
    x='Year:O',
    y='curr_cost:Q',
    color=alt.value('firebrick')  # Bar color
).add_selection(
    nearest
)

# Combine the charts
chart = alt.layer(line_cov, line_cost).resolve_scale(
    y='independent'
)

st.altair_chart(chart, use_container_width=True)


