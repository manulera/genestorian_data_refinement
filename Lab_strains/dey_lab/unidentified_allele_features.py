#%%
import json
import re

with open('alleles.json') as f:
    allele_feature_list = json.load(f) 
for allele in allele_feature_list:
    pattern = allele['pattern']
    strings = re.split(r'ALLELE|GENE|TAG|MARKER|PROMOTER', pattern)
    print(strings)
# %%
