import pandas as pd
import numpy as np

# import data file
data = pd.read_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\ParameterData_Main.txt', sep='\t')

# remove objects out of gate ('R01')
data = data[data['R01'] == 1].reset_index(drop=True)

# add 'Strain' column to data
strains_list = list(pd.read_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\strain names.csv')['Strain'])
data['Strain'] = data['Well '].replace(list(range(1, 52)), strains_list)
# remove 'Blank' strain (empty wells)
data = data[data['Strain'] != 'blank'].reset_index(drop=True)

# sample 500 cells from each strain
unique_strains = pd.unique(data['Strain'])
sampled_data_dict = {}
for s in unique_strains:
    strain_data = data[data['Strain'] == s]
    if len(strain_data) > 500:
        sampled_data_dict[s] = strain_data.sample(n=500)
    if 50 < len(strain_data) < 500:  # less then 50 cells => empty well (ignore strain)
        sampled_data_dict[s] = data[data['Strain'] == s]
# Append sampled_data_dict to one dataframe:
sampled_data = pd.DataFrame()
for k in sampled_data_dict:
    sampled_data = sampled_data.append(sampled_data_dict[k], ignore_index=True)
# export sampled_data to csv file
sampled_data.to_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\sampled data.csv', index=False)

# get mean to each strain:
# create and fill new dataframe
strains_mean = pd.DataFrame()
strains_mean['Strain'] = pd.unique(sampled_data['Strain'])
strains_mean['Mean Intensity 405nm'] = np.nan
strains_mean['Mean Intensity 488nm'] = np.nan
for s2 in strains_mean['Strain']:
    strains_mean.loc[strains_mean['Strain'] == s2, 'Mean Intensity 405nm'] = sampled_data[sampled_data['Strain'] == s2]['Mean Intensity 405nm'].mean()
    strains_mean.loc[strains_mean['Strain'] == s2, 'Mean Intensity 488nm'] = sampled_data[sampled_data['Strain'] == s2]['Mean Intensity 488nm'].mean()
# save strains mean to csv
strains_mean.to_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\Strains Mean Intensity.csv', index=False)


