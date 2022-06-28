# %%
import toml
import pandas as pd
import json

data = pd.read_csv('strains.tsv', sep='\t')


def feature_dict(toml_file):
    # a dictionary in which the keys are name, synonyms and toml_keys and values are toml_keys
    synonyms_2toml_key_dict = {}
    feature_type_dict = toml.load(toml_file)
    feature_type_name = list(feature_type_dict.keys())[0]
    # a dictionary in which the keys are toml keys and value is a dictionary of name, ref, sy
    toml_key_2feature = feature_type_dict[feature_type_name]
    for feature_key in toml_key_2feature:
        if 'name' in toml_key_2feature[feature_key]:
            name = toml_key_2feature[feature_key]['name']
            synonyms_2toml_key_dict[name] = feature_key
        if 'synonyms' in toml_key_2feature[feature_key]:
            synonyms = toml_key_2feature[feature_key]['synonyms']
            for synonym in synonyms:
                synonyms_2toml_key_dict[synonym] = feature_key
        synonyms_2toml_key_dict[feature_key] = feature_key
    return synonyms_2toml_key_dict


def replace_allele_features(toml_file, genotypes, replace_word):
    features = feature_dict(toml_file)
    genotype_features_replaced = []
    matches = []
    for genotype in genotypes:
        for feature in features.keys():
            if feature.lower() in genotype.lower():
                matches.append(feature)
        matches.sort(key=len, reverse=True)
        for match in matches:
            genotype = genotype.replace(match, replace_word)
        genotype_features_replaced.append(genotype)

    return genotype_features_replaced


data['Genotype'] = data['Genotype'].astype(str)
genotypes_allele_replaced = replace_allele_features(
    '../../data/alleles.toml', data['Genotype'], 'ALLELE')
genotypes_gene_replaced = replace_allele_features(
    '../../data/gene_IDs.toml', genotypes_allele_replaced, 'GENE')
genotypes_tag_replaced = replace_allele_features(
    '../../allele_components/tags.toml', genotypes_gene_replaced, 'TAG')

genotypes_marker_replaced = replace_allele_features(
    '../../allele_components/markers.toml', genotypes_tag_replaced, 'MARKER')

with open('first_version_pipeline.txt', 'w', encoding='utf-8') as out:
    for replaced_genotype in genotypes_marker_replaced:
        out.write(f'{replaced_genotype}\n')

# %%
