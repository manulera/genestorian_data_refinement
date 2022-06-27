# %%
import re
import toml


def feature_name(toml_file):
    f = toml.load(toml_file)
    feature = list(f.keys())
    return feature[0]


def gene_dict(toml_file):
    gene_dict = {}
    f = toml.load(toml_file)
    systematic_id = f['gene'].keys()
    for id in systematic_id:
        if 'name' in f['gene'][id].keys():
            names = f['gene'][id]['name']
            gene_dict.update({names: id})
        if 'synonyms' in f['gene'][id].keys():
            synonym = f['gene'][id]['synonyms']
            for sy in synonym:
                gene = re.match(r'[a-z]{3}\d+', sy)
                systematic_id = re.match(r'SP.+\.\d+c?', sy)
                gene_dict[gene] = id
                gene_dict[gene] = systematic_id
    return gene_dict


def allele_dict(toml_file):
    allele_dict = {}
    f = toml.load(toml_file)
    allele_list_toml = f['allele'].keys()
    #allele_list_toml.sort(key=len, reverse=True)

    for alleles in allele_list_toml:
        allele_ref_id = f['allele'][alleles]['ref']
        if allele_ref_id not in allele_dict.keys():
            allele_dict.update({alleles: allele_ref_id})

    #allele_dict.keys().sort(key=len, reverse=True)
    return allele_dict


def other_dict(toml_file, replace_word):
    feature = replace_word.lower()
    other_feature_dict = {}
    f = toml.load(toml_file)

    feature_list_toml = f[feature].keys()

    other_feature_dict.update({feature: [feature_list_toml]})
    return other_feature_dict


def is_allele(allele_dict, genotype, replace_word):
    alleles = []
    for allele in genotype:
        for a in allele_dict.keys():
            if a in allele.lower():
                allele = allele.replace(a.lower(), replace_word)
                alleles.append(allele)

    return alleles


def is_gene(gene_dict, genotype, replace_word):
    genes = []
    for allele in genotype:
        for name in re.findall(r'[a-z]{3}\d+', allele):
            if name.lower() in gene_dict.keys():
                allele = allele.replace(name, replace_word)
                genes.append(allele)
    print(genes)
    return genes


def is_other(genotype, other_feature_dict, replace_word):
    genotype = []
    feature = replace_word.lower()
    for alleles in genotype:
        for keys in other_feature_dict.keys():
            if keys in alleles:
                alleles = alleles.replace(keys, replace_word)
        genotype.append(alleles)
    return genotype


def replace_allele_features(toml_file, genotype, replace_word):
    feature_to_replace = feature_name(toml_file)
    if feature_to_replace == 'gene':
        gene_DICTIONARY = gene_dict(toml_file)
        replaced_word = is_gene(gene_DICTIONARY, genotype, replace_word)
    if feature_to_replace == 'allele':
        alleledict = allele_dict(toml_file)
        replaced_word = is_allele(alleledict, genotype, replace_word)
    else:
        feature_dict = other_dict(toml_file, replace_word)
        replaced_word = is_other(genotype, feature_dict, replace_word)
    return replaced_word


# %%
genotype = ['cls1-36 ase1-GFP:KanMx6']
genotype_a = replace_allele_features(
    '../../data/alleles.toml', genotype, 'ALLELE')
print(genotype_a)


# %%
genotype_g = replace_allele_features(
    '../../data/gene_IDs.toml', genotype_a, 'GENE')
print(genotype_g)

# %%
# %%
# %%
