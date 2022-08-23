#%%
from genestorian_module import excel_to_tsv
import pandas as pd

read_file = pd.read_excel('SR Strain List.xlsx', na_filter=False)
read_file['strain_id'] = read_file.iloc[:, 0]
read_file['SEXUAL TYPE'] = read_file['SEXUAL TYPE'].astype(str)
read_file['GENOTYPE'] = read_file['GENOTYPE'].astype(str)
read_file['genotype'] = read_file['SEXUAL TYPE'] + " " + read_file['GENOTYPE']
read_file.to_excel('post_processed.xlsx')

# %%
excel_to_tsv('post_processed.xlsx', ['strain_id', 'genotype'], 'strains.tsv')
# %%
