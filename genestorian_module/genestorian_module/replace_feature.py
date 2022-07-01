import toml


def feature_dict(toml_file):
    # dictionary in which the keys are name,synonyms,toml_keys and values are toml_keys
    synonyms_2toml_key_dict = {}
    feature_type_dict = toml.load(toml_file)
    feature_type_name = list(feature_type_dict.keys())[0]
    # dictionary in which the keys are toml keys and value is a dictionary of name, ref, sy
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
                matches.append(feature.lower())
        matches.sort(key=len, reverse=True)
        for match in matches:
            genotype = genotype.replace(match, replace_word)
        genotype_features_replaced.append(genotype)

    return genotype_features_replaced

# Similar to replace_allele_features but also returns list of subsituted feature names


def replaced_allele_feature_name(toml_file, genotypes, replace_word):
    features = feature_dict(toml_file)
    genotype_with_replaced_names = []
    matches = []
    genotype_replaced_feature = []
    for genotype in genotypes:
        for feature in features.keys():
            if feature.lower() in genotype.lower():
                matches.append(feature.lower())
        matches.sort(key=len, reverse=True)
        for match in matches:
            if match in genotype:
                genotype_replaced_feature.append(match)
            genotype = genotype.replace(match, replace_word)
        genotype_with_replaced_names.append(genotype)

    return [genotype_with_replaced_names, genotype_replaced_feature]
