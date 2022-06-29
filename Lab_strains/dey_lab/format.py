# %%
import pandas as pd

read_file = pd.read_excel('Manu_Strains.xlsx', usecols=[
                          'Sample Name', 'Genotype'], na_filter=False)

inconsistent_char_list = ['‚àÜ0', 'Œî']


for i in range(len(read_file['Genotype'])):
    for inconsistent_char in inconsistent_char_list:
        if inconsistent_char in read_file['Genotype'][i]:
            read_file['Genotype'][i] = read_file['Genotype'][i].replace(
                inconsistent_char, 'Δ')

read_file.to_csv('strains.tsv', sep='\t')
