import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import os
from vega_datasets import data


from data_clean import combined_df, hpv_df
df = combined_df()
df2 = hpv_df()



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
    title='Yearly Comparison of Current and Project Cost'
)


st.write("# Yearly Comparison of Current and Project Cost")
st.altair_chart(stacked_bar_chart, use_container_width=True)
# user input for filtering
selected_assumption = st.selectbox("Select Assumption Type", options=df2['assumption_type'].unique())
# Filter data based on selection
filtered_df = df2[df2['assumption_type'] == selected_assumption]
# stacked bar chart for visualization
stacked_bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x='year:N',  # Year is nominal data
    y=alt.Y('sum(value):Q', stack='zero'),  # Stack the values of cancer_prevented and deaths_prevented
    color='metric:N',  # Color by metric (cancer_prevented or deaths_prevented)
    tooltip=['year:N', 'region:N', 'income_group:N', 'metric:N', 'sum(value):Q']
).properties(
    title='Comparison of Cancer Prevented and Deaths Prevented by Year'
)

# display the chart 
st.title('Cancer/death Data Visualization')
st.altair_chart(stacked_bar_chart, use_container_width=True)

## Set up basic world map as template backgorund
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 400
height  = 200
project = 'equirectangular'

map_background = alt.Chart(source
).mark_geoshape(
    fill = '#aaa',
    stroke = 'white'
).properties(
    width = width,
    height = height
).project(project)

map_background

