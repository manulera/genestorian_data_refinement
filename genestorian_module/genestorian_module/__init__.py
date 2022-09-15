import pandas as pd


def excel_to_tsv(excel_file, read_cols, tsv_file):
    '''Extracts genotype and strain id from excel file to tsv file

            Parameter:
                excel_file(path to file): path to the excel file
                read_cols(list) : list of coloumn names to be read
                tsv_file(path): path to tsv file

            Returns:
                None'''
    #read_cols = ['strain_id/Sample Name', 'genotype']
    read_file = pd.read_excel(excel_file, usecols=read_cols, na_filter=False)
    read_file = read_file.rename(
        columns={read_cols[0]: 'strain_id', read_cols[1]: 'genotype'})

    read_file['strain_id'] = read_file['strain_id'].astype(str)
    read_file['genotype'] = read_file['genotype'].astype(str)

    inconsistent_char_list = ['‚àÜ0', 'Œî']

    for i in range(len(read_file['genotype'])):
        for inconsistent_char in inconsistent_char_list:
            if inconsistent_char in read_file['genotype'][i]:
                read_file['genotype'][i] = read_file['genotype'][i].replace(
                    inconsistent_char, 'Δ')

    read_file.to_csv(tsv_file, sep='\t', index=False)
    return None


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
