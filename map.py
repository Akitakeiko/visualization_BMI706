import altair as alt
from vega_datasets import data

## Set up basic world map as template backgorund
source = alt.topo_feature(data.world_110m.url, 'countries')

width = 400
height  = 200
project = 'equirectangular'

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
            from_ = alt.LookupData(data_subset, 'country-code', ['country_name','year','possible_cancer_cases']),
        )

    cases_scale = alt.Scale(domain=[data_full['possible_cancer_cases'].min(), data_full['possible_cancer_cases'].max()], type = 'log') #we want the domain to stay the same regardless of subset
    cases_color = alt.Color(field = 'possible_cancer_cases', type = 'quantitative', scale = cases_scale)
    chart_cases = chart_base_map.mark_geoshape().encode(
        color = cases_color,
        tooltip = ['country_name:N', 'possible_cancer_cases:Q']
        ).properties(
        title=f'HPV cases worldwide in {selected_year}'
    )

    HPV_cases_map = alt.vconcat(map_background + chart_cases
    ).resolve_scale(
        color = 'independent'
    )

    return HPV_cases_map


