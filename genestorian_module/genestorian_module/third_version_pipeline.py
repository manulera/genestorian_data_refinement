from genestorian_module.read_and_write import read_strains_tsv
from genestorian_module.replace_feature import build_feature_dict
import re
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

            for replaced_allele_feature in replaced_allele_features:
                # The same feature may appear several times, we create an element in the list for each of them:
                for coords in find_feature_coords(allele_dict['name'], replaced_allele_feature):
                    replaced_feature_dict = {}
                    replaced_feature_dict['name'] = replaced_allele_feature
                    replaced_feature_dict['feature_type'] = feature_name
                    replaced_feature_dict['coords'] = coords

                    allele_dict['allele_features'].append(
                        replaced_feature_dict)
                    allele_features_sorted = sorted(allele_dict['allele_features'],
                                                    key=itemgetter('coords'), reverse=False)
                    allele_dict['allele_features'] = allele_features_sorted
    return output_list


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
