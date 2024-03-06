import numpy as np
import pandas as pd

def combined_df():
    df = pd.read_csv('/Users/akitakeiko/visualization_BMI706/data/combined_dfall.csv', index_col = 0)
    return df

def hpv_df():
    hpv_past = pd.read_csv("/Users/akitakeiko/visualization_BMI706/data/hpv_past_results.csv", index_col = 0)
    hpv_2020 = pd.read_csv("/Users/akitakeiko/visualization_BMI706/data/hpv_2020s_results.csv", index_col = 0)
    id_vars = ['region', 'income_group', 'year', 'assumption_type']
    value_vars = ['coverage', 'cancer_prevented', 'deaths_prevented', 'possible_cancer_cases', 'possible_cancer_deaths']
    
    hpv_past_melted = df_one.melt(id_vars=id_vars, value_vars=value_vars, var_name='metric', value_name='value')
    hpv_2020_melted = df_two.melt(id_vars=id_vars, value_vars=value_vars, var_name='metric', value_name='value')
    
    # Combine the melted DataFrames
    df2 = pd.concat([hpv_past_melted, hpv_2020_melted])
    return df2

