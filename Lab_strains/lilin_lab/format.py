#%%
from genestorian_module import excel_to_tsv
import pandas as pd

read_file = pd.read_excel('DY-export-2.xlsx', na_filter=False)
read_file['DY number'] = read_file['DY number'].astype(str)
read_file['strain_id'] = 'DY' + read_file['DY number']
read_file.to_excel('post_processed.xlsx')

# %%
excel_to_tsv('post_processed.xlsx', ['strain_id', 'Genotype'], 'strains.tsv')
# %%
