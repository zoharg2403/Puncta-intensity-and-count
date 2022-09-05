import pandas as pd
import numpy as np

# read data .csv files
cell_data = pd.read_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\ParameterData_Main.txt', sep='\t')
pun_data = pd.read_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\ParameterData_puncta_lipid droplet.txt', sep='\t')

# remove cells out of gate
cell_data = cell_data[cell_data['R01'] == 1]
pun_data = pun_data[pun_data['MO.R01'] == 1]

# add strain column to cell_data and pun_data
strains_list = list(pd.read_csv(r'C:\Users\zoharga\Desktop\Zohar\plot\Reut - for ines 170522\strain names.csv')['Strain'])
cell_data['Strain'] = cell_data['Well '].replace(list(range(1, 52)), strains_list)
pun_data['Strain'] = pun_data['Well '].replace(list(range(1, 52)), strains_list)

# remove 'blank' strain
cell_data = cell_data[cell_data['Strain'] != 'blank']
pun_data = pun_data[pun_data['Strain'] != 'blank']

# count # puncta per cell
pun_per_cell = pd.DataFrame()
pun_per_cell[['Object ID', 'Strain']] = cell_data[['Object ID', 'Strain']]
pun_per_cell['# pun in cell'] = np.nan
for r in pun_per_cell['Object ID']:
    pun_per_cell.loc[pun_per_cell['Object ID'] == r, '# pun in cell'] = pun_data[pun_data['Parent Object ID (MO)'] == r].shape[0]
# AVG # puncta per cell - according to strain
pun_per_strain = pd.DataFrame()
pun_per_strain['Strain'] = pd.unique(pun_per_cell['Strain'])
pun_per_strain['# puncta per cell in strain'] = np.nan
for s in pun_per_strain['Strain']:
    pun_per_strain.loc[pun_per_strain['Strain'] == s, '# puncta per cell in strain'] = pun_per_cell.loc[pun_per_cell['Strain'] == s, '# pun in cell'].mean()
pun_per_cell.to_csv('number of punctas per cell.csv', index=False)
pun_per_strain.to_csv('mean number of punctas per strain.csv', index=False)

# AVG puncta per cell (total pun/total cells per strain)
new_df = pd.DataFrame()
new_df['Strain'] = pd.unique(cell_data['Strain'])
new_df['Cells Num'] = np.nan
new_df['Puncta Num'] = np.nan
for s in new_df['Strain']:
    new_df.loc[new_df['Strain'] == s, 'Cells Num'] = cell_data[cell_data['Strain'] == s].shape[0]
    new_df.loc[new_df['Strain'] == s, 'Puncta Num'] = pun_data[pun_data['Strain'] == s].shape[0]
new_df['Ratio - #puncta/#cell'] = new_df['Puncta Num'] / new_df['Cells Num']
new_df.to_csv('mean number of punctas per strain - total puncta count div by total cell count.csv', index=False)
