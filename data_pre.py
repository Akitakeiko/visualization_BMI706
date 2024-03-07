### These data pre-processing steps were performed on local python environment 
### then export to csv and upload in the data folder

import pandas as pd

country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})

df=pd.read_csv("Data/combined_cohort.csv")



df_merged = pd.merge(df, country_df[['Country', 'country-code']], on='Country', how='left')

df_cleaned = df_merged.dropna(subset=['country-code'])

df_cleaned.to_csv('Data/country-code_cohort.csv', index=False)
