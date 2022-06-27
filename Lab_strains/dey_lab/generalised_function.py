# %%
import re
import toml
import json


def feature_name(toml_file):
    f = toml.load(toml_file)
    feature = list(f.keys())
    return feature[0]


def feature_dict(toml_file):
    feature_dict = {}
    f = toml.load(toml_file)
    toml_key_name = feature_name(toml_file)
    toml_keys = f[toml_key_name].keys()
    for toml_key in toml_keys:
        if 'name' in f[toml_key_name][toml_key].keys():
            names = f[toml_key_name][toml_key]['name']
            feature_dict.update({names: toml_key})
        if 'synonyms' in f[toml_key_name][toml_key].keys():
            synonym = f[toml_key_name][toml_key]['synonyms']
            for sy in synonym:
                feature_dict[sy] = toml_key
    return feature_dict


def replace_allele_features(toml_file, genotype, replace_word):
    features = feature_dict(toml_file)
    alleles = []
    for allele in genotype:
        for a in features.keys():
            if a.lower() in allele.lower():
                allele_r = allele.replace(a, replace_word)
                alleles.append(allele_r)
                break
    if len(alleles) == 0:
        alleles.append(genotype)
    return alleles


genotype = ['cls1-36 ase1-GFP:KanMx6']

genotype_g = replace_allele_features(
    '../../data/gene_IDs.toml', genotype, 'GENES')
print(genotype_g)

genotype_t = replace_allele_features(
    '../../allele_components/tags.toml', genotype_g, 'TAGS')


genotype_m = replace_allele_features(
    '../../allele_components/markers.toml', genotype_t, 'MARKERS')

print(genotype_m)


# %%
