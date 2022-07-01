import pandas as pd


def read_strains_tsv(tsv_file):
    data = pd.read_csv(tsv_file, sep='\t', na_filter=False)
    data['Genotype'] = data['Genotype'].astype(str)
    data['Genotype'] = data['Genotype'].str.lower()
    return data
