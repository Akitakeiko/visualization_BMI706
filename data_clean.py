import numpy as np
import pandas as pd

def combined_df():
    df = pd.read_csv('/Users/akitakeiko/visualization_BMI706/data/combined_dfall.csv', index_col = 0)
    return df

def hpv_df():
    df2 = pd.read_csv("/Users/akitakeiko/visualization_BMI706/data/hpv_past_results.csv", index_col = 0)
    return df2