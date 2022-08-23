
import pandas as pd

read_file = pd.read_csv('strains_raw.tsv', usecols=[
                        'NBRPID', 'genotype'], na_filter=False, sep='\t')
read_file = read_file.rename(
    columns={'NBRPID': 'strain_id'})
read_file.to_csv('strains.tsv', sep='\t', index=False)

