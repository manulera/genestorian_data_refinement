# %%
import json


def build_common_pattern_dict(in_json_file):
    with open(in_json_file) as f:
        data = json.load(f)
    occurances_dict = {}
    for allele_dict in data:
        pattern = allele_dict['pattern']
        allele_name = allele_dict['name']
        if pattern in occurances_dict.keys():
            occurances_dict[pattern].append(allele_name)
        else:
            occurances_dict[pattern] = [allele_name]
    return occurances_dict


occurances_dict = build_common_pattern_dict('alleles.json')

with open('occurances.json', 'w') as fp:
    json.dump(occurances_dict, fp, indent=3)

# %%
