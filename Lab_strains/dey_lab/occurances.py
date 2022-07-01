#%% 
import re
import json
import pandas as pd

allele_names = set([])
data = pandas.read_csv('strains.tsv', sep='\t', usecols=['Genotype'])

# We force conversion to string, otherwise empty values are parsed as nans (floats)
data['Genotype'] = data['Genotype'].astype(str)
for genotype in data.Genotype:
    # split the genotype by any separator and add the alleles names to the set
    allele_names.update([a.lower() for a in re.split("\s+", genotype)])
