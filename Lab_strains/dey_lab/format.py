# %%
import json
import re
import pandas as pd
import toml


read_file = pd.read_excel('Manu_Strains.xlsx', usecols=[
                          'Sample Name', 'Genotype'])
read_file.to_csv('strains.tsv', sep='\t')

data = pd.read_csv('strains.tsv', sep='\t')
allele_names = set({})
genotype_dict = {}
data['Genotype'] = data['Genotype'].astype(str)
for genotype in data.Genotype:
    allele_names.update([a.lower() for a in re.split("\s+", genotype)])
    genotype_dict.update({genotype: [a.lower()
                         for a in re.split("\s+", genotype)]})

print(len(genotype_dict))
# print(allele_names)

# %%
allele_dict = {}
f = toml.load('../../data/alleles.toml')
allele_list_toml = f['allele'].keys()

for alleles in allele_list_toml:
    allele_ref_id = f['allele'][alleles]['ref']
    if allele_ref_id not in allele_dict.keys():
        allele_dict.update({allele_ref_id: [alleles]})
    else:
        allele_dict.setdefault(allele_ref_id).append(alleles)


for key in allele_dict:
    allele_dict[key].sort(key=len, reverse=True)

# %%
systematic_ids = set()
gene_names = set()
other = set()
gene_dictionary = dict()


def add_gene_name(gene_name):
    if re.match(r'[a-z]{3}\d+', gene_name) is not None:
        gene_names.add(gene_name)
    elif re.match(r'SP.+\.\d+c?', gene_name) is not None:
        systematic_ids.add(gene_name)
    else:
        other.add(gene_name)


with open('../../data/gene_IDs_names.tsv') as ins:
    # First line does not count
    ins.readline()
    for line in ins:
        fields = line.strip().split('\t')
        add_gene_name(fields[0])
        gene_dictionary[fields[0]] = fields[0]
        if len(fields) > 1:
            add_gene_name(fields[1])
            gene_dictionary[fields[1]] = fields[0]
            if len(fields) > 2:
                if ',' in fields[2]:
                    [add_gene_name(f) for f in fields[2].split(',')]
                    for f in fields[2].split(','):
                        add_gene_name(f)
                        gene_dictionary[f] = fields[0]
                else:
                    add_gene_name(fields[2])
                    gene_dictionary[fields[2]] = fields[0]

# %%


def is_allele(allele, allele_dict, gene_dictionary):
    alleles = []
    for allele in genotype_dict[genotype]:
        for name in re.findall(r'[a-z]{3}\d+', allele):
            if name in gene_names:
                systematic_id = gene_dictionary[name]
                allele_found = False
                if systematic_id in allele_dict:
                    for published_allele in allele_dict[systematic_id]:
                        if published_allele.lower() in allele:
                            allele = allele.replace(
                                published_allele.lower(), 'ALLELE')
                            allele_found = True
                            break

                if not allele_found:
                    allele = allele.replace(name, 'GENE')
        alleles.append(allele)
    return alleles

# %%


allele_dictonary = {}
genotype_dictonary = {}
for genotype in genotype_dict.keys():

    allele_r = is_allele(genotype, allele_dict, gene_dictionary)
    genotype_dictonary.update({genotype: allele_r})


# %%
with open('format.json', 'w') as fp:
    json.dump(genotype_dictonary, fp, indent=3)
