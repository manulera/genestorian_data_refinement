data = pd.read_csv('strains.tsv', sep='\t')
allele_names = set({})
genotype_dict = {}
data['Genotype'] = data['Genotype'].astype(str)
for genotype in data.Genotype:
    allele_names.update([a.lower() for a in re.split("\s+", genotype)])
    genotype_dict.update({genotype: [a.lower()
                         for a in re.split("\s+", genotype)]})

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


f = toml.load('../../data/gene_IDs.toml')
gene_dictionary = {}
systematic_id = f['gene'].keys()
for id in systematic_id:
    if 'name' in f['gene'][id].keys():
        names = f['gene'][id]['name']
        gene_dictionary.update({names: id})
    if 'synonyms' in f['gene'][id].keys():
        synonym = f['gene'][id]['synonyms']
        for sy in synonym:
            gene = re.match(r'[a-z]{3}\d+', sy)
            systematic_id = re.match(r'SP.+\.\d+c?', sy)
            gene_dictionary[gene] = id
            gene_dictionary[gene] = systematic_id


# %%


def is_allele(allele, allele_dict, gene_dictionary):
    alleles = []
    for allele in genotype_dict[genotype]:
        print(allele)
        for name in re.findall(r'[a-z]{3}\d+', allele):
            if name in gene_dictionary.keys():
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
    print(genotype)

    allele_r = is_allele(genotype, allele_dict, gene_dictionary)
    genotype_dictonary.update({genotype: allele_r})


# %%
with open('format.json', 'w') as fp:
    json.dump(genotype_dictonary, fp, indent=3)
