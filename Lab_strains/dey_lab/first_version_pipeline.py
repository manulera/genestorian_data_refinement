# %%
from genestorian_module.replace_feature import replace_allele_features
import pandas as pd


genotype = ['cls1-36 ase1-GFP:Kan', 'SPAC1002.01']
genotype_a = replace_allele_features(
    '../../data/alleles.toml', genotype, 'ALLELE')
print(genotype_a)
genotype_g = replace_allele_features(
    '../../data/gene_IDs.toml', genotype_a, 'GENE')
print(genotype_g)


genotype_t = replace_allele_features(
    '../../allele_components/tags.toml', genotype_g, 'TAG')

print(genotype_t)
genotype_m = replace_allele_features(
    '../../allele_components/markers.toml', genotype_t, 'MARKER')

print(genotype_m)


# %%
data = pd.read_csv('strains.tsv', sep='\t', na_filter=False)


data['genotype'] = data['genotype'].astype(str)
genotype_list = []
for genotype in data['genotype']:
    genotype_list.append(genotype.lower())


genotypes_allele_replaced = replace_allele_features(
    '../../data/alleles.toml', genotype_list, 'ALLELE')
genotypes_gene_replaced = replace_allele_features(
    '../../data/gene_IDs.toml', genotypes_allele_replaced, 'GENE')
genotypes_tag_replaced = replace_allele_features(
    '../../allele_components/tags.toml', genotypes_gene_replaced, 'TAG')

genotypes_marker_replaced = replace_allele_features(
    '../../allele_components/markers.toml', genotypes_tag_replaced, 'MARKER')

with open('first_version_pipeline.txt', 'w', encoding='utf-8') as out:
    for replaced_genotype in genotypes_marker_replaced:
        out.write(f'{replaced_genotype}\n')

# %%
