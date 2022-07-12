# %%
from genestorian_module import excel_to_tsv
import pandas as pd

read_file = pd.read_excel('pombe strains_20210413.xlsx', na_filter=False)
read_file['AP/PT '] = read_file['AP/PT '].astype(str)
read_file['Glycerol number'] = read_file['Glycerol number'].astype(str)
read_file['strain_id'] = read_file['AP/PT '] + read_file['Glycerol number']
read_file.to_excel('post_processed.xlsx')
excel_to_tsv('post_processed.xlsx', [
             'strain_id', 'Genotype'], 'strains.tsv')
