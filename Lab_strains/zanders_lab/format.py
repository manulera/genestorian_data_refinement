#%%
from genestorian_module import excel_to_tsv
import pandas as pd

read_file = pd.read_excel('yeastJune 2021.xlsx', na_filter=False)
read_file['SEZY'] = read_file['SEZY'].astype(str)
read_file['strain_id']= 'SEZY' + read_file['SEZY']
read_file.to_excel('post_processed.xlsx')
# %%
excel_to_tsv('post_processed.xlsx', ['strain_id', 'genotype'], 'strains.tsv')

# %%
