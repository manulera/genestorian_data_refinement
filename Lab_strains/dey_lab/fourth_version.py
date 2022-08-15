# %%
import collections
from genestorian_module import read_strains_tsv
from genestorian_module.replace_feature import build_feature_dict
import re
import json
from operator import itemgetter

# %%


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
with open('strains.json', 'w', encoding="utf-8") as fp:
    json.dump(strain_list, fp, indent=3, ensure_ascii=False)


# %%


def build_replaced_feature_tag(feature_dict, allele, replace_word):
    matches = []
    allele_features_matched = []
    returns = []
    for feature in feature_dict.keys():
        if feature.lower() in allele:
            matches.append(feature.lower())
    matches.sort(key=len, reverse=True)
    for match in matches:
        if match in allele:
            allele_features_matched.append(match)
            allele = allele.replace(match, replace_word)
    for allele_feature_matched in allele_features_matched:
        returns.append((allele_feature_matched, replace_word))
    return returns, allele


def build_replaced_feature_tag2(feature_dict, allele_pattern, replace_word):
    matches = []
    allele_features_matched = []
    returns = []
    for feature in feature_dict.keys():
        if feature.lower() in allele_pattern:
            matches.append(feature.lower())
    matches.sort(key=len, reverse=True)


def identify_other(pattern):
    others = []
    split_alleles = re.split(
        r'ALLELE|GENE|TAG|MARKER|PROMOTER|-|:|::|<<|--', pattern)
    for element in split_alleles:
        if len(element) != 0:
            others.append((element, 'other'))
    return others


def identify_separator(allele_name):
    separators = ['-', ':', '::', '<<', '--']
    matched_separators = []
    for separator in separators:
        if separator in allele_name:
            matched_separators.append((separator, '-'))
    return matched_separators


def sort_pattern(pattern_list, allele_name):
    pattern_dict = {}
    pattern_list = (
        sorted(pattern_list, key=lambda x: len(x[0]), reverse=True))
    for feature in pattern_list:
        coords = [i.start() for i in re.finditer(
            re.escape(feature[0]), allele_name)]
        for coord in coords:
            pattern_dict[coord] = feature
            replace_word = len(feature[0])*'@'
            allele_name = allele_name.replace(feature[0], replace_word)
    pattern_list = collections.OrderedDict(sorted(pattern_dict.items()))
    return list(pattern_list.values())


def build_pattern_nltk_tag(allele_names, toml_files):
    output_list = []
    for allele_name in allele_names:
        output_list.append({
            'name': allele_name,
            'pattern': [],
            'replaced_feature': allele_name
        })
    for toml_file in toml_files:
        feature_dict, feature_name = build_feature_dict(toml_file)
        for allele_dict in output_list:

            new_features = build_replaced_feature_tag(
                feature_dict, allele_dict['replaced_feature'], feature_name)
            allele_dict['replaced_feature'] = new_features[1]
            if len(new_features) != 0:
                for new_feature in new_features[0]:
                    allele_dict['pattern'].append(new_feature)
    for allele_dict in output_list:
        separators = identify_separator(allele_dict['replaced_feature'])
        if len(separators) != 0:
            for separator in separators:
                allele_dict['pattern'].append(separator)
        others = identify_other(allele_dict['replaced_feature'])
        if len(others) != 0:
            for other_element in others:
                allele_dict['pattern'].append(other_element)
        allele_dict['pattern'] = sort_pattern(
            allele_dict['pattern'], allele_dict['name'])
    return output_list
# %%


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

alleles_list = build_pattern_nltk_tag(allele_names, toml_files)

with open('allele_nltk.json', 'w', encoding="utf-8") as fp:
    json.dump(alleles_list, fp, indent=3, ensure_ascii=False)


# %%
def funct(feature_dict, allele_pattern, allele_name, replace_word):
    matches = []
    allele_features_matched = []
    returns = []
    if len(allele_pattern) == 0:
        allele_pattern.append(allele_name)
    for allele in allele_pattern:
        for feature in feature_dict.keys():
            if feature.lower() in allele:
                matches.append(feature.lower())
        for match in matches:
            if match in allele:
                allele_features_matched.append(match)
                alleles = re.split(
                    match, allele)
                for allele in alleles:
                    returns.append(allele)
    for allele_feature_matched in allele_features_matched:
        returns.append((allele_feature_matched, replace_word))
    print(returns)
    return returns


def build_pattern_nltk_tag(allele_names, toml_files):
    output_list = []
    for allele_name in allele_names:
        output_list.append({
            'name': allele_name,
            'pattern': []
        })
    for toml_file in toml_files:
        feature_dict, feature_name = build_feature_dict(toml_file)
        for allele_dict in output_list:

            new_features = funct(
                feature_dict, allele_dict['pattern'], allele_dict['name'], feature_name)
            allele_dict['pattern'] = new_features
            if len(new_features) != 0:
                for new_feature in new_features[0]:
                    allele_dict['pattern'].append(new_feature)
    return None


build_pattern_nltk_tag(allele_names, toml_files)


# %%
