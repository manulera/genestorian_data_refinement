# %%
import re
import toml
import json


def feature_dict(toml_file):
    feature_dict = {}
    f = toml.load(toml_file)
    feature_name = list(f.keys())[0]

    feature_keys = f[feature_name].keys()
    for feature_key in feature_keys:
        if 'name' in f[feature_name][feature_key].keys():
            name = f[feature_name][feature_key]['name']
            feature_dict[name] = feature_key
        if 'synonyms' in f[feature_name][feature_key].keys():
            synonyms = f[feature_name][feature_key]['synonyms']
            for synonym in synonyms:
                feature_dict[synonym] = feature_key
    return feature_dict


def replace_allele_features(toml_file, genotype, replace_word):
    features = feature_dict(toml_file)
    alleles = []
    matches = []
    for allele in genotype:
        for feature in features.keys():
            if feature.lower() in allele.lower():
                if feature != '':
                    matches.append(feature)
        for feature in features.values():
            if feature.lower() in allele.lower() and feature.lower() not in matches:
                matches.append(feature)
        matches.sort(key=len, reverse=True)
        i = 0
        while i < len(matches):
            a = matches[i]
            allele = allele.replace(a, replace_word)
            i += 1
        alleles.append(allele)

    if len(alleles) == 0:
        return genotype
    return alleles


genotype = ['cls1-36 ase1-GFP:KanMx6', 'SPAC1002.01']
genotype_a = replace_allele_features(
    '../../data/alleles.toml', genotype, 'ALLELE')
print(genotype_a)
genotype_g = replace_allele_features(
    '../../data/gene_IDs.toml', genotype_a, 'GENES')
print(genotype_g)


# %%
genotype_t = replace_allele_features(
    '../../allele_components/tags.toml', genotype_g, 'TAGS')

print(genotype_t)
genotype_m = replace_allele_features(
    '../../allele_components/markers.toml', genotype_t, 'MARKERS')

print(genotype_m)
