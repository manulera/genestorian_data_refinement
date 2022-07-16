# %%
import json
import re
from collections import Counter
import pandas as pd

with open('alleles.json') as f:
    allele_feature_list = json.load(f)
unidentified_allele_feature_list = []
for allele in allele_feature_list:
    pattern = allele['pattern']
    split_alleles = re.split(r'ALLELE|GENE|TAG|MARKER|PROMOTER', pattern)
    unidentified_allele_feature_list = (
        unidentified_allele_feature_list + split_alleles)

df_unidentified_feature_occurences = pd.DataFrame(Counter(unidentified_allele_feature_list).items(), columns=[
    'feature', 'no_of_occurence'])
df_unidentified_feature_occurences = df_unidentified_feature_occurences.sort_values(
                                            'no_of_occurence', ascending=False)
df_unidentified_feature_occurences.to_csv(
    'unidentified_allele_feature.tsv', sep='\t', index=False)

# %%
