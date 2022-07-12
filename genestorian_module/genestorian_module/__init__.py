import pandas as pd


def excel_to_tsv(excel_file, read_cols, tsv_file):
    #read_cols = ['strain_id/Sample Name', 'genotype']
    read_file = pd.read_excel(excel_file, usecols=read_cols, na_filter=False)
    read_file = read_file.rename(
        columns={read_cols[0]: 'Strain_id', read_cols[1]: 'Genotype'})
    inconsistent_char_list = ['‚àÜ0', 'Œî']

    for i in range(len(read_file['Genotype'])):
        for inconsistent_char in inconsistent_char_list:
            if inconsistent_char in read_file['Genotype'][i]:
                read_file['Genotype'][i] = read_file['Genotype'][i].replace(
                    inconsistent_char, 'Δ')

    read_file.to_csv(tsv_file, sep='\t')
    return None


def read_strains_tsv(tsv_file):
    data = pd.read_csv(tsv_file, sep='\t', na_filter=False)
    data['Genotype'] = data['Genotype'].astype(str)
    data['Genotype'] = data['Genotype'].str.lower()
    return data
