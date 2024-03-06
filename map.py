import altair as alt
from vega_datasets import data

## Set up basic world map as template backgorund
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 600
height  = 300
project = 'equirectangular'

background = alt.Chart(source
).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=width,
    height=height
).project(project)

def return_income_map(df_cleaned):
    chart_base = alt.Chart(source
    ).properties(
        width=600,
        height=300
    ).project(project
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df_cleaned, "country-code", ['Country', 'income_group']),
    )

    income_group = alt.Color('income_group:N',type='nominal')


    chart_rate = chart_base.mark_geoshape().encode(
    color= income_group,
    tooltip=["income_group:N", "Country:N"]

    ).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_cleaned, 'country-code', ['Country', 'income_group'])
    ).properties(
    title='Income group Worldwide'
    )
    
    income_map = alt.vconcat(background+chart_rate
    ).resolve_scale(
        color = 'independent'
    ) 
             
    return income_map



def return_world_map(df_cleaned, selected_year):
    if (df_cleaned.shape[0] == 0):
        return background.properties(title=f'HPV cases worldwide in {selected_year}')
    
    case_scale = alt.Scale(domain=[df_cleaned['possible_cancer_cases'].min(), df_cleaned['possible_cancer_cases'].max()], scheme='oranges')
    rate_color = alt.Color(field="possible_cancer_cases", type="quantitative", scale=case_scale)

    chart_base = alt.Chart(source
    ).properties(
        width=width,
        height=height
    ).project(project
    ).transform_lookup(
        lookup="id",
        from_=alt.LookupData(df_cleaned, "country-code", ['Country', 'income_group', 'possible_cancer_cases']),
    )
    chart_case = chart_base.mark_geoshape().encode(
    color= rate_color,
    tooltip=["possible_cancer_cases:Q", "Country:N"]
    ).transform_lookup(
    lookup='id',
    from_=alt.LookupData(df_cleaned, 'country-code', ['Country','possible_cancer_cases'])
    ).properties(
        title=f'HPV cases worldwide in {selected_year}'
    )
    
    cases_map = alt.vconcat(background+chart_case
    ).resolve_scale(
        color = 'independent'
    ) 
             
    return cases_map
    
    
