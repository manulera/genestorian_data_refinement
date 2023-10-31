#%%
from genestorian_module.read_and_write import excel_to_tsv
excel_to_tsv('Manu_Strains.xlsx', ['Sample Name', 'Genotype'], 'strains.tsv')


