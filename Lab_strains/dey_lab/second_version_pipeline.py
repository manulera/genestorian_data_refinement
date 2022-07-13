# %%
from genestorian_module import read_strains_tsv
from genestorian_module.replace_feature import build_feature_dict
import re
import json
from operator import itemgetter


def build_strain_list(strain_tsv_file):
    data = read_strains_tsv(strain_tsv_file)
    strain_list = list()

    # Iterate over rows
    for row_index, strain in data.iterrows():
        alleles = list()
        mating_type = 'h?'  # use this as empty value
        for allele in re.split("\s+", strain['genotype']):
            # Sometimes people use h? to indicate that mating type is unkwown
            # TODO : found h0 in the allele list. Ask Manu is it a mating type
            if allele in ['h90', 'h-', 'h+', 'h?']:
                mating_type = allele
            else:
                alleles.append(allele)

        strain_list.append({
            'id': strain['strain_id'],
            'genotype': strain['genotype'],
            'mating_type': mating_type,
            'alleles': alleles
        })
    return strain_list


strain_list = build_strain_list('strains.tsv')
with open('strains.json', 'w') as fp:
    json.dump(strain_list, fp, indent=3, ensure_ascii=False)


# %%

def build_replaced_feature_dict(feature_dict, allele, replace_word):
    matches = []
    allele_features_matched = []
    for feature in feature_dict.keys():
        if feature.lower() in allele:
            matches.append(feature.lower())
    matches.sort(key=len, reverse=True)
    for match in matches:
        if match in allele:
            allele_features_matched.append(match)
            allele = allele.replace(match, replace_word)
    return allele, allele_features_matched


def find_feature_coords(allele, feature):
    if '+' in feature:
        feature = re.escape(feature)
    coords = [(i.start(), i.end()) for i in re.finditer(feature, allele)]
    return coords


def build_allele_feature_list(allele_names, toml_files):
    output_list = []
    for allele_name in allele_names:
        output_list.append({
            'name': allele_name,
            'pattern': allele_name,
            'allele_features': []
        })
    for toml_file in toml_files:
        feature_dict, feature_name = build_feature_dict(toml_file)
        for allele_dict in output_list:
            new_pattern, replaced_allele_features = build_replaced_feature_dict(
                feature_dict, allele_dict['pattern'], feature_name)
            allele_dict['pattern'] = new_pattern
            if len(replaced_allele_features) != 0:
                for replaced_allele_feature in replaced_allele_features:
                    replaced_feature_dict = {}
                    replaced_feature_dict['name'] = replaced_allele_feature
                    replaced_feature_dict['feature_type'] = feature_name
                    replaced_feature_dict['coords'] = find_feature_coords(
                        allele_dict['name'], replaced_allele_feature)

                    allele_dict['allele_features'].append(
                        replaced_feature_dict)
                    allele_features_sorted = sorted(allele_dict['allele_features'],
                                                    key=itemgetter('coords'), reverse=False)
                    allele_dict['allele_features'] = allele_features_sorted
    return output_list


toml_files = [
    '../../data/alleles.toml',
    '../../data/gene_IDs.toml',
    '../../allele_components/tags.toml',
    '../../allele_components/markers.toml',
    '../../allele_components/promoters.toml'
]

strain_list = build_strain_list('strains.tsv')
allele_names = set({})
for strain in strain_list:
    allele_names.update(strain['alleles'])

alleles_list = build_allele_feature_list(allele_names, toml_files)

with open('alleles.json', 'w') as fp:
    json.dump(alleles_list, fp, indent=3, ensure_ascii=False)


# %%


def find_common_pattern(alleles_list):
    occurences_dict = {}
    for allele_dict in alleles_list:
        pattern = allele_dict['pattern']
        allele_name = allele_dict['name']
        if pattern in occurences_dict:
            occurences_dict[pattern].append(allele_name)
        else:
            occurences_dict[pattern] = [allele_name]
    return occurences_dict


occurences_dict = find_common_pattern(alleles_list)
with open('occurences2.json', 'w') as fp:
    json.dump(occurences_dict, fp, indent=3, ensure_ascii=False)
