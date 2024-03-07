### These datasets are generally cleaned adn imported in csv format from the data folder
### Except for hpv vaccine data, which is re-processed here.

import numpy as np
import pandas as pd

def vaccine_df():
    df = pd.read_csv('https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/combined_dfall.csv', index_col = 0)
    return df

def hpv_df():
    hpv_past = pd.read_csv("https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/hpv_past_results.csv", index_col = 0)
    hpv_2020 = pd.read_csv("https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/hpv_2020s_results.csv", index_col = 0)
    id_vars = ['region', 'income_group', 'year', 'assumption_type']
    value_vars = ['cancer_prevented', 'deaths_prevented', 'possible_cancer_cases', 'possible_cancer_deaths']
    
    hpv_past_melted = hpv_past.melt(id_vars=id_vars, value_vars=value_vars, var_name='metric', value_name='value')
    hpv_2020_melted = hpv_2020.melt(id_vars=id_vars, value_vars=value_vars, var_name='metric', value_name='value')
    
    # Combine the melted DataFrames
    df2 = pd.concat([hpv_past_melted, hpv_2020_melted])
    return df2

def cohort_df():
    df3 = pd.read_csv("https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/combined_cohort.csv", index_col = 0)
    return df3

def country_df():
    df4 = pd.read_csv("https://raw.githubusercontent.com/Akitakeiko/visualization_BMI706/main/Data/country-code_cohort.csv")
    return df4