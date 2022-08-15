from genestorian_module.replace_feature import build_feature_dict
from genestorian_module.third_version_pipeline import build_strain_list
import re
import json
import sys
import os


def build_separators_dict():
    separators_dict = {}
    with open("../../allele_components/separators.txt", "r") as fp:
        for x in fp:
            separators_dict[x] = 'separator'
    return separators_dict


def add_other_tag(pattern_list):
    for feature in pattern_list:
        if type(feature) != list:
            idx = pattern_list.index(feature)
            pattern_list[idx] = [feature, 'other']
    return pattern_list


def replace_allele_features(feature_dict, pattern_list, feature_name, matches):
    out_list = list()
    for i in range(len(pattern_list)):
        if type(pattern_list[i]) != str:
            out_list.append(pattern_list[i])
            continue
        if len(matches) == 0:
            for feature in feature_dict.keys():
                if feature.lower() in pattern_list[i]:
                    matches.append(feature.lower())
            matches.sort(key=len, reverse=True)
        allele_substring = pattern_list[i]
        this_list = [allele_substring]
        for match in matches:
            if match in allele_substring:
                start = allele_substring.find(match)
                end = start + len(match)
                this_list = [allele_substring[:start], [
                    allele_substring[start:end], feature_name], allele_substring[end:]]
                # Remove empty strings
                this_list = list(filter(lambda x: x != '', this_list))
                this_list = replace_allele_features(
                    feature_dict, this_list, feature_name, matches)
                break
        out_list += this_list

    return out_list


def build_nltk_tag(allele_names, toml_files):
    output_list = []
    for allele_name in allele_names:
        output_list.append({
            'name': allele_name,
            'pattern': [allele_name],
        })
    for toml_file in toml_files:
        feature_dict, feature_name = build_feature_dict(toml_file)
        for allele_dict in output_list:
            allele_dict['pattern'] = replace_allele_features(
                feature_dict, allele_dict['pattern'], feature_name, [])

    separators_dict = build_separators_dict()
    for allele_dict in output_list:
        # replace separators
        allele_dict['pattern'] = replace_allele_features(
            separators_dict, allele_dict['pattern'], '-', [])
        # add other tags to untagged elements:
        allele_dict['pattern'] = add_other_tag(allele_dict['pattern'])
    return output_list


def prettier_json(input_dict):
    output_str = json.dumps(input_dict, indent=3, ensure_ascii=False)

    match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]', output_str)
    while match is not None:
        new_string = re.sub('\n', ' ', match.group())
        new_string = re.sub('\s+', ' ', new_string)
        output_str = output_str[:match.start()] + \
            new_string + output_str[match.end():]
        match = re.search(r'\[(?=\n)(\n|(?![{}]).)+\]', output_str)
    return output_str


def main(input_file):
    strain_list = build_strain_list(input_file)
    allele_names = set({})
    for strain in strain_list:
        allele_names.update(strain['alleles'])
    toml_files = [
        '../../data/alleles.toml',
        '../../data/gene_IDs.toml',
        '../../allele_components/tags.toml',
        '../../allele_componenets/tags_fpbase.toml'
        '../../allele_components/markers.toml',
        '../../allele_components/promoters.toml'
    ]
    alleles_list = build_nltk_tag(allele_names, toml_files)
    output_file_name = 'alleles_nltk.json'
    output_dir = os.path.dirname(input_file)
    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, 'w', encoding="utf-8") as fp:
        fp.write(prettier_json(alleles_list))

    return None


if __name__ == "__main__":
    input_file = sys.argv[1]
    main(input_file)
