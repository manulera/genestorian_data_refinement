# %%
import toml

toml_dict = {'gene': dict()}

with open('../data/gene_IDs_names.tsv') as ins:
    for line in ins:
        ls = line.strip().split('\t')
        systematic_gene_id = ls[:1]
        if len(ls[1:2]) == 0:
            if len(ls[2:3]) == 0:
                toml_dict['gene'][systematic_gene_id[0]] = {
                    'ref': systematic_gene_id[0],
                }
            else:
                synonyms = ls[2:3]
                toml_dict['gene'][systematic_gene_id[0]] = {
                    'ref': systematic_gene_id[0],
                    'synonyms': synonyms
                }
        else:
            main_gene_name = ls[1:2]
            if len(ls[2:3]) == 0:
                toml_dict['gene'][systematic_gene_id[0]] = {
                    'ref': systematic_gene_id[0],
                    'name': main_gene_name[0]
                }
            else:
                synonyms = ls[2:3]
                toml_dict['gene'][systematic_gene_id[0]] = {
                    'ref': systematic_gene_id[0],
                    'name': main_gene_name[0],
                    'synonyms': synonyms
                }
with open('../data/gene_IDs.toml', "w") as toml_file:
    toml.dump(toml_dict, toml_file)

# %%
