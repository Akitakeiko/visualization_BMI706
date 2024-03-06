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
""" 
def return_world_map(df_cleaned, selected_year):
    chart_base_map = alt.Chart(source
        ).properties( 
            width = width,
            height = height
        ).project(project
        ).transform_lookup(
            lookup = 'id',
            from_ = alt.LookupData(df_cleaned, 'country-code', ['Country','year','possible_cancer_cases']),
        )

    cases_scale = alt.Scale(domain=[df_cleaned['possible_cancer_cases'].min(), df_cleaned['possible_cancer_cases'].max()], scheme='oranges') #we want the domain to stay the same regardless of subset
    cases_color = alt.Color(field = 'possible_cancer_cases:Q', type = 'quantitative', scale = cases_scale)
    chart_cases = chart_base_map.mark_geoshape().encode(
        color = cases_color,
        tooltip = ['Country:N', 'possible_cancer_cases:Q']
        ).properties(
        title=f'HPV cases worldwide in {selected_year}'
    )

    cases_map = alt.vconcat(background + chart_cases
    ).resolve_scale(
        color = 'independent'
    )

    return cases_map """



def return_world_map(df_cleaned, selected_year, width=500, height=300):
    # Filter data for the selected year
    df_year = df_cleaned[df_cleaned['year'] == selected_year]

    # If there's no data after filtering, we can't proceed
    if df_year.empty:
        # Display a text message over the background map
        return alt.Chart(source).mark_geoshape().encode(
            tooltip=None
        ).properties(
            title=f'No HPV cases data available for {selected_year}',
            width=width,
            height=height
        ).project(
            type='equirectangular'
        )

    # Calculate min and max values for the current year to set the scale
    min_cases = df_year['possible_cancer_cases'].min()
    max_cases = df_year['possible_cancer_cases'].max()

    # Define the color scale based on possible_cancer_cases
    cases_scale = alt.Scale(domain=[min_cases, max_cases], scheme='oranges')

    # Create the base of the map using the world geometry
    chart_base_map = alt.Chart(source).mark_geoshape(
    ).encode(
        color=alt.Color('properties.possible_cancer_cases:Q', scale=cases_scale, legend=alt.Legend(title="HPV Cancer Cases"))
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(df_year, 'country-code', ['possible_cancer_cases'])
    ).project(
        type='equirectangular'
    ).properties(
        width=width,
        height=height
    )

    # Adding tooltip for interactivity
    chart_cases = chart_base_map.encode(
        tooltip=['properties.possible_cancer_cases:Q']
    ).properties(
        title=f'HPV cases worldwide in {selected_year}'
    )
    
    cases_map = alt.vconcat(background + chart_cases
    ).resolve_scale(
        color = 'independent'
    )

    return cases_map

