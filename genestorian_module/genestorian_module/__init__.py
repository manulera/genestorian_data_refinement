
import pandas as pd


def read_strains_tsv(strain_csv_file):
    data = pd.read_csv(strain_csv_file, sep='\t')
    data['Genotype'] = data['Genotype'].astype(str)
    data['Genotype'] = data['Genotype'].str.lower()
    data['Sample Name'] = data['Sample Name'].astype(str)
    return data
