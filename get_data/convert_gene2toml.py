# %%
import toml
import re

toml_dict = {'gene': dict()}

with open('../data/gene_IDs_names.tsv') as ins:
    for line in ins:
        ls = line.strip().split('\t')
        systematic_gene_id = ls[0]
        toml_dict['gene'][systematic_gene_id] = {
            'ref': systematic_gene_id,
        }

        if len(ls) > 1 and ls[1] != '':
            toml_dict['gene'][systematic_gene_id]['name'] = ls[1]

        if len(ls) > 2 and ls[2] != '':
            synonyms = re.split(",", ls[2])
            toml_dict['gene'][systematic_gene_id]['synonyms'] = synonyms
with open('../data/gene_IDs.toml', "w") as toml_file:
    toml.dump(toml_dict, toml_file)


# %%
