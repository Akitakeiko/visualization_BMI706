import altair as alt
import pandas as pd
import streamlit as st
import os


### P1.2 ###

# Move this code into `load_data` function {{


# }}


@st.cache
def load_data():
    df = pd.read_csv("combined_dfall.csv")
    
    return df



df = load_data()
df2= pd.read_csv("hpv_past_results.csv")
df3= pd.read_csv("combined_cohort.csv")

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




st.write("## final project task2")



# Create a heatmap instead of a bar chart

year= st.slider('year', 2010, 2010, 2020)
subset = df3[df3["year"] == year]

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








