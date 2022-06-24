# %%
import toml

# %%
toml_dict = {'allele': dict()}

with open('../data/alleles_pombemine.tsv') as ins:
    for line in ins:
        ls = line.strip().split('\t')
        # For now we skip alleles with delta in them. In the future we may
        # have to consider some rec12 / rec8 allele was mentioned in some
        # issue that had an equivalent name
        if 'delta' not in ls[2]:
            systematic_id, main_gene_name, allele_name = ls[:3]
            toml_dict['allele'][allele_name] = {
                'name': allele_name,
                'ref': systematic_id
            }

with open('../data/alleles.toml', "w") as toml_file:
    toml.dump(toml_dict, toml_file)
