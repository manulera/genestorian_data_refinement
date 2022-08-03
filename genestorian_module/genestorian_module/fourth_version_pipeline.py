import collections
from genestorian_module.replace_feature import build_feature_dict
from genestorian_module.third_version_pipeline import build_strain_list
import re
import json
import sys
import os


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


def identify_other(pattern):
    others = []
    split_alleles = re.split(
        r'ALLELE|GENE|TAG|MARKER|PROMOTER|-|:|::|<<|--', pattern)
    for element in split_alleles:
        if len(element) != 0:
            others.append((element, 'other'))
    return others


def identify_separator(allele_name):
    separators = ['--', '::', ':', '<<', '-']
    matched_separators = []
    for separator in separators:
        if separator in allele_name:
            matched_separators.append((separator, '-'))
    return matched_separators


def sort_pattern(pattern_list, allele_name):
    pattern_dict = {}
    for items in pattern_list:

        coords = [i.start() for i in re.finditer(
            re.escape(items[0]), allele_name)]
        for coord in coords:
            pattern_dict[coord] = items
    pattern_list = collections.OrderedDict(sorted(pattern_dict.items()))
    return list(pattern_list.values())


def build_nltk_tag(allele_names, toml_files):
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

            # Manu: You can do this without using the replace string. For example:
            # ase1-GFP > [['GENE', 'ase1'], '-GFP']
            # Next time you can iterate over the list elements and take only those
            # that are not lists, and replace on '-GFP' only.
            new_features = build_replaced_feature_tag(
                feature_dict, allele_dict['replaced_feature'], feature_name)
            allele_dict['replaced_feature'] = new_features[1]
            # Manu: no need to check if list is empty when iterating, if it's empty it won't iterate
            # if len(new_features) != 0:
            for new_feature in new_features[0]:
                allele_dict['pattern'].append(new_feature)
    for allele_dict in output_list:
        separators = identify_separator(allele_dict['name'])
        if len(separators) != 0:
            for separator in separators:
                allele_dict['pattern'].append(separator)
        others = identify_other(allele_dict['replaced_feature'])
        if len(others) != 0:
            for other_element in others:
                allele_dict['pattern'].append(other_element)
        allele_dict['pattern'] = sort_pattern(
            allele_dict['pattern'], allele_dict['name'])
        allele_dict = allele_dict.pop('replaced_feature')
    return output_list

# Nicer output to get the whole pattern in a single line
def prettier_json(input_dict):
    output_str = json.dumps(input_dict, indent=3, ensure_ascii=False)

    match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]',output_str)
    while match is not None:
        new_string = re.sub('\n',' ',match.group())
        new_string = re.sub('\s+',' ',new_string)
        output_str = output_str[:match.start()] + new_string+ output_str[match.end():]
        match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]',output_str)
    return output_str

def main(input_file):
    strain_list = build_strain_list(input_file)
    allele_names = set({})
    for strain in strain_list:
        allele_names.update(strain['alleles'])
    toml_files = toml_files = [
        '../../data/alleles.toml',
        '../../data/gene_IDs.toml',
        '../../allele_components/tags.toml',
        '../../allele_components/markers.toml',
        '../../allele_components/promoters.toml'
    ]
    alleles_list = build_nltk_tag(allele_names, toml_files)
    output_file_name = 'alleles_nltk.json'
    # Manu: less hacky
    output_dir = os.path.dirname(input_file)
    # Manu: it's the path of a file, not a directory
    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, 'w', encoding="utf-8") as fp:
        fp.write(prettier_json(alleles_list))

    return None


if __name__ == "__main__":
    # MANU: Better to extract args here and pass a meaningful argument to main
    input_file = sys.argv[1]
    main(input_file)
