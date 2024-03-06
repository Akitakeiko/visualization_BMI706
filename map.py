import altair as alt
from vega_datasets import data

## Set up basic world map as template backgorund
""" source = alt.topo_feature(data.world_110m.url, 'countries')

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
 """

def return_world_map(data_subset, data_full, selected_year):
    if (data_subset.shape[0] == 0):
        return map_background.properties(title=f'HPV cases worldwide in {selected_year}')

    chart_base_map = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(data_subset, 'code', ['country_name','year','possible_cancer_cases']),
        )

    cases_scale = alt.Scale(domain=[data_full['possible_cancer_cases'].min(), data_full['possible_cancer_cases'].max()], type = 'log') #we want the domain to stay the same regardless of subset
    cases_color = alt.Color(field = 'sum(possible_cancer_cases)', type = 'quantitative', scale = cases_scale)
    chart_cases = chart_base_map.mark_geoshape().encode(
        color = cases_color,
        tooltip = ['country_name:N', 'sum(possible_cancer_cases):Q']
        ).properties(
        title=f'HPV cases worldwide in {selected_year}'
    )

    HPV_cases_map = alt.vconcat(map_background + chart_cases
    ).resolve_scale(
        color = 'independent'
    )

    return HPV_cases_map



source = alt.topo_feature(data.world_110m.url, 'countries')

project = 'equirectangular'

background = alt.Chart(source
).mark_geoshape(
    fill='#aaa',
    stroke='white'
).properties(
    width=600,
    height=300
).project(project)

def return_income_map(data):
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
    title='Cancer Mortality Rate Worldwide'
    )
    
    income_map = alt.vconcat(background+chart_rate
    ).resolve_scale(
        color = 'independent'
    ) 
             
return income_map