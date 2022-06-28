# %%
import toml


def feature_dict(toml_file):
    #a dictionary in which the keys are name, synonyms and toml_keys and values are toml_keys 
    synonyms_2toml_key_dict = {}
    feature_type_dict = toml.load(toml_file)
    feature_type_name = list(feature_type_dict.keys())[0]
    #a dictionary in which the keys are toml keys and value is a dictionary of name, ref, sy
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
                if feature != '':
                    matches.append(feature)
        matches.sort(key=len, reverse=True)
        for match in matches:
            genotype = genotype.replace(match, replace_word)
        genotype_features_replaced.append(genotype)

    return genotype_features_replaced


genotype = ['cls1-36 ase1-GFP:KanMx6', 'SPAC1002.01']
genotype_a = replace_allele_features(
    '../../data/alleles.toml', genotype, 'ALLELE')
print(genotype_a)
genotype_g = replace_allele_features(
    '../../data/gene_IDs.toml', genotype_a, 'GENE')
print(genotype_g)


# %%
genotype_t = replace_allele_features(
    '../../allele_components/tags.toml', genotype_g, 'TAG')

print(genotype_t)
genotype_m = replace_allele_features(
    '../../allele_components/markers.toml', genotype_t, 'MARKER')

print(genotype_m)

# %%
