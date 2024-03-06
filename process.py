import altair as alt
import pandas as pd
import streamlit as st
import os
import numpy as np

### P1.2 ###

# Move this code into `load_data` function {{


# }}

from data_clean import combined_df, hpv_df, cohort_df
df = combined_df()
df2 = hpv_df()
df3 = cohort_df() 


df3['death_per_100k'] = (df3['possible_cancer_deaths'] / df3['cohort_size']) * 100000
df3['case_per_100k'] = (df3['possible_cancer_cases'] / df3['cohort_size']) * 100000

df3['ratio']=df3['possible_cancer_deaths']/df3['possible_cancer_cases']

df3['normalized_deaths'] = df3.apply(lambda row: 
                                     row['death_per_100k'] / 276 if row['income_group'] == 'Low income' 
                                     else (row['death_per_100k'] / 612 if row['income_group'] == 'High income' 
                                     else (row['death_per_100k'] / 576 if row['income_group'] == 'Upper middle income' 
                                     else (row['death_per_100k'] / 648 if row['income_group'] == 'Lower middle income' 
                                     else row['death_per_100k']))),
                                     axis=1)
df3['normalized_cases'] = df3.apply(lambda row: 
                                     row['case_per_100k'] / 276 if row['income_group'] == 'Low income' 
                                     else (row['case_per_100k'] / 612 if row['income_group'] == 'High income' 
                                     else (row['case_per_100k'] / 576 if row['income_group'] == 'Upper middle income' 
                                     else (row['case_per_100k'] / 648 if row['income_group'] == 'Lower middle income' 
                                     else row['case_per_100k']))),
                                     axis=1)

st.set_page_config(
    layout="wide",
	initial_sidebar_state = "auto", 
	page_title = "HPV dashboard",
    page_icon = '/Users/akitakeiko/visualization_BMI706/img/hpv.png'
)


st.write("## final project task2")

# Slider for year
year= st.slider('year', 2010, 2010, 2020)
subset = df3[df3["year"] == year]

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

bar_chart_cohort = alt.Chart(subset).mark_bar(color='steelblue').encode(
    x=alt.Y('sum(cohort_size):Q', title='Sum of cohort size'),
    y=alt.X('country_name:N', title='Country', sort='-x'),
    tooltip=['country_name', 'sum(cohort_size)']
).properties(
    title='Cohort Size by Country'
)

bar_chart_cases = alt.Chart(subset).mark_bar(color='pink').encode(
    x=alt.Y('sum(possible_cancer_cases):Q', title='Sum of HPV cases'),
    y=alt.X('country_name:N', title='Country', sort='-x'),
    tooltip=['country_name', 'sum(possible_cancer_cases)']
).properties(
    title='Possible HPV Cancer Cases by Country'
)

st.write("## HPV cases vs. cohort sizes")
st.altair_chart(bar_chart_cohort, use_container_width=True)
st.altair_chart(bar_chart_cases, use_container_width=True)

# Create a piechart 
pie = alt.Chart(subset).mark_arc(innerRadius=50).encode(
    theta='sum(normalized_deaths):Q',
    color= 'income_group:N',
    tooltip=['income_group', 'sum(normalized_deaths)']
).properties(
    title='cancer deaths in each income group',
    width=220,  # Reduced width
    height=220

)

pie2 = alt.Chart(subset).mark_arc(innerRadius=50).encode(
    theta='sum(normalized_cases):Q',
    color= 'income_group:N',
    tooltip=['income_group', 'sum(normalized_cases)']
).properties(
    title='cancer cases in each income group',
     width=220,  # Reduced width
    height=220
)

donut = alt.hconcat(pie, pie2).resolve_scale(
    # two donut charts should use different color schema
    color='independent'
)

donut



chart = alt.Chart(df3).mark_bar().encode(
    x=alt.X('income_group:N', axis=alt.Axis(title='', labels=False)),  # Remove x-axis label
    y=alt.Y('mean(ratio):Q', title='Case/Death Ratio'),  # Adjusted for case/death ratio
    color=alt.Color('income_group:N', scale=alt.Scale(
        domain=['Low income', 'Upper middle income', 'Lower middle income', 'High income'],
        range=['#add8e6', '#87ceeb', '#4682b4', '#00008b']  # Light to deep blue
    )),
    column='year:O'  # Separate bars into columns by year
).properties(
    width=45,  # Adjust the width of each bar chart
    height=150  # And the height of the chart
)

chart


df3 = df3.dropna(subset=['cohort_size'])




incomegroup = st.radio("Select Income group for trend line", ('Low income', 'Lower middle income','Upper middle income','High income'))
subset = df3[df3["income_group"] == incomegroup]




income1 = alt.Chart(subset).mark_line(point=True,color='blue').encode(
    x=alt.X('year:O', axis=alt.Axis(title='Year')),
    y=alt.Y('sum(death_per_100k):Q', axis=alt.Axis(title='death_per_100k')),
    tooltip=['year:O', alt.Tooltip('sum(death_per_100k):Q', title='Total Deaths')]
).properties(
    title= "Trend of death per 100k per income group",
    width=700,
    height=250
)

income2 = alt.Chart(subset).mark_line(point=True,color='green').encode(
    x=alt.X('year:O', axis=alt.Axis(title='Year')),
    y=alt.Y('sum(case_per_100k):Q', axis=alt.Axis(title='death_per_100k')),
    tooltip=['year:O', alt.Tooltip('sum(case_per_100k):Q', title='Total Deaths')]
).properties(
    title= "Trend of case per 100k per income group",
    width=700,
    height=250
)

income1
income2

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
    title='Yearly Comparison of Current and Projected Cost'
)

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






