### These data pre-processing steps were performed on local python environment 
### then export to csv and upload in the data folder

import pandas as pd


df1= pd.read_csv('Data/yearly-results/results_2010.csv')
df2= pd.read_csv('Data/yearly-results/results_2011.csv')
df3= pd.read_csv('Data/yearly-results/results_2012.csv')
df4= pd.read_csv('Data/yearly-results/results_2013.csv')
df5= pd.read_csv('Data/yearly-results/results_2014.csv')
df6= pd.read_csv('Data/yearly-results/results_2015.csv')
df7= pd.read_csv('Data/yearly-results/results_2016.csv')
df8= pd.read_csv('Data/yearly-results/results_2017.csv')
df9= pd.read_csv('Data/yearly-results/results_2018.csv')
df10=pd.read_csv('Data/yearly-results/results_2019.csv')
df11=pd.read_csv('Data/yearly-results/results_2020.csv')


df12= pd.read_csv('Data/projections_with_2021_rate/results_curr_2022.csv')
df13= pd.read_csv('Data/projections_with_2021_rate/results_curr_2023.csv')
df14= pd.read_csv('Data/projections_with_2021_rate/results_curr_2024.csv')
df15= pd.read_csv('Data/projections_with_2021_rate/results_curr_2025.csv')
df16= pd.read_csv('Data/projections_with_2021_rate/results_curr_2026.csv')
df17= pd.read_csv('Data/projections_with_2021_rate/results_curr_2027.csv')
df18= pd.read_csv('Data/projections_with_2021_rate/results_curr_2028.csv')
df19= pd.read_csv('Data/projections_with_2021_rate/results_curr_2029.csv')
df20= pd.read_csv('Data/projections_with_2021_rate/results_curr_2030.csv')
df21=pd.read_csv('Data/projections_with_2021_rate/results_curr_2021.csv')


dfs = [df1, df2, df3, df4, df5, df6, df7, df8, df9,df10,df21,df12,df13,df14,df15,df16,df17,df18,df19,df20,df21]

start_year = 2010

for i, df in enumerate(dfs):
    df['year'] = start_year + i


combined_df = pd.concat(dfs, ignore_index=True)

# New dataset 1: output combined_dfall.csv
combined_df.to_csv('Data/combined_dfall.csv', index=False)

df22=pd.read_csv('Data/hpv_past_results.csv')



result_df = pd.merge(df22, combined_df[['country_name', 'year', 'cohort_size','']], on=['country_name', 'year'], how='left')


#New dataset 2 : output combined_cohort.csv
result_df.to_csv('Data/combined_cohort.csv', index=False)


country_df = pd.read_csv('https://raw.githubusercontent.com/hms-dbmi/bmi706-2022/main/cancer_data/country_codes.csv', dtype = {'conuntry-code': str})

df=pd.read_csv("Data/combined_cohort.csv")



df_merged = pd.merge(df, country_df[['Country', 'country-code']], on='Country', how='left')

df_cleaned = df_merged.dropna(subset=['country-code'])
#New dataset 3: output country-code_cohort.csv
df_cleaned.to_csv('Data/country-code_cohort.csv', index=False)
