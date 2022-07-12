# %%
import json


def build_common_pattern_dict(in_json_file):
    with open(in_json_file) as f:
        data = json.load(f)
    occurences_dict = {}
    for allele_dict in data:
        pattern = allele_dict['pattern']
        allele_name = allele_dict['name']
        if pattern in occurences_dict.keys():
            occurences_dict[pattern].append(allele_name)
        else:
            occurences_dict[pattern] = [allele_name]
    return occurences_dict


occurences_dict = build_common_pattern_dict('alleles.json')

with open('occurances.json', 'w') as fp:
    json.dump(occurences_dict, fp, indent=3)

# %%
