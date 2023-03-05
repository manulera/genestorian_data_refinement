import pandas as pd

def read_strains_tsv(tsv_file):
    '''
    Reads the genotype and strain_id coloumn from strain.tsv file

        Parameter:
            tsv_file(path): path to strains.tsv 

        Return:
            data(pandas dataframe): pandas dataframe where columns are strain_id and genotype 
    '''
    data = pd.read_csv(tsv_file, sep='\t', na_filter=False)
    data['genotype'] = data['genotype'].astype(str)
    data['strain_id'] = data['strain_id'].astype(str)
    data['genotype'] = data['genotype'].str.lower()
    return data