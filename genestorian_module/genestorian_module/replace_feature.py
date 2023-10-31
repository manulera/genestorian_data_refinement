import toml
from genestorian_module.read_and_write import read_strains_tsv
import re


def build_feature_dict(toml_file):
    '''
    Builds a dictionary from input toml file

    Parameter:
        toml_file(toml): toml file of an allele feature(gene, allele, marker etc)

    Returns:
        synonyms_2toml_key_dict(dict): dict of name and synonyms of the features are keys and the name are the values
        feature_type_name(str) : name of the feature(eg: gene, allele, marker etc)
         '''
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
    return synonyms_2toml_key_dict, feature_type_name.upper()


def build_strain_list(strain_tsv_file):
    '''
    Builds a dict of strains where keys are strain_id, genotype, mating type 
    and alleles and save them in a list

    Parameter:
        strains_tsv_file(tsv file): strains.tsv which contains strain_id and genotype

    Returns:
        strain_list(list): list of dictionaries
    '''
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
