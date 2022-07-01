# %%
#from genestorian_module import read_strains_tsv
from genestorian_module import read_strain_tsv
from genestorian_module.replace_feature import replaced_allele_feature_name
import pandas as pd
import re
import json


def strains_list(strain_tsv_file):
    data = read_strain_tsv(strain_tsv_file)
    strain_list = list()

    # Iterate over rows
    for row_index, strain in data.iterrows():
        alleles = list()
        mating_type = 'h?'  # use this as empty value
        for allele in re.split("\s+", strain['Genotype']):
            # Sometimes people use h? to indicate that mating type is unkwown
            if allele in ['h90', 'h-', 'h+', 'h?']:
                mating_type = allele
            else:
                alleles.append(allele)

        strain_list.append({
            'id': strain['Sample Name'],
            'genotype': strain['Genotype'],
            'mating_type': mating_type,
            'alleles': alleles
        })
    return strain_list


strain_list = strains_list('strains.tsv')
with open('strains.json', 'w') as fp:
    json.dump(strain_list, fp, indent=3)


# %%


def feature_name(name_list, feature_type, features_list):
    for name in name_list:
        feature_dict = {}
        feature_dict['name'] = name
        feature_dict['feature_type'] = feature_type
        features_list.append(feature_dict)
    return features_list


def allele_feature_list(allele_names, allele_toml_File,
                        gene_toml_file, tag_toml_file,
                        marker_toml_file, promoter_toml_file):
    allele_dict = {}
    for allele_name in allele_names:
        allele_pattern_dict = {}
        # list of replaced allele and allele feature names list
        allele_name_replaced = replaced_allele_feature_name(
            allele_toml_File, [allele_name.lower()], 'ALLELE')
        allele_names = allele_name_replaced[1]
        features_list = feature_name(allele_names, 'Allele', [])
        # list of replaced genes and gene feature names list
        allele_gene_replaced = replaced_allele_feature_name(
            gene_toml_file, allele_name_replaced[0], 'GENE')
        gene_names = allele_gene_replaced[1]
        features_list = feature_name(gene_names, 'Gene', features_list)
        # list of replaced tags and tag feature names list
        allele_tag_replaced = replaced_allele_feature_name(
            tag_toml_file, allele_gene_replaced[0], 'TAG')
        tag_names = allele_tag_replaced[1]
        features_list = feature_name(tag_names, 'Tag', features_list)
        # list of markers replaced and marker feature names list
        allele_marker_replaced = replaced_allele_feature_name(
            marker_toml_file, allele_tag_replaced[0], 'MARKER')
        marker_names = allele_marker_replaced[1]
        features_list = feature_name(marker_names, 'Marker', features_list)
        # list of promoters replaced and promoter feature names list
        allele_promoter_replaced = replaced_allele_feature_name(
            promoter_toml_file, allele_marker_replaced[0], 'PROMOTER')
        promoter_names = allele_promoter_replaced[1]
        features_list = feature_name(promoter_names, 'Promoter', features_list)

        pattern = allele_promoter_replaced[0]
        allele_pattern_dict['name'] = allele_name
        allele_pattern_dict['pattern'] = pattern
        allele_pattern_dict['allele_features'] = features_list
        allele_dict[allele_name] = allele_pattern_dict
    return list(allele_dict.values())


data = read_strain_tsv('strains.tsv')
allele_names = set([])
data['Genotype'] = data['Genotype'].astype(str)
for genotype in data.Genotype:
    allele_names.update([a.lower()
                        for a in re.split("\s+", genotype) if a != ''])

alleles_list = allele_feature_list(allele_names, '../../data/alleles.toml',
                                   '../../data/gene_IDs.toml',
                                   '../../allele_components/tags.toml',
                                   '../../allele_components/markers.toml',
                                   '../../allele_components/promoters.toml')

with open('alleles.json', 'w') as fp:
    json.dump(alleles_list, fp, indent=3)
