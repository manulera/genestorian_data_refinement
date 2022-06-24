#%%
import toml


def feature_name(toml_file):
    f = toml.load(toml_file)
    feature = list(f.keys())
    return feature[0]
    

def replace_allele_features( feature_toml_file, genotype, feature):
    f = toml.load(feature_toml_file)
    feature = feature_name(feature_toml_file)
    feature_list_toml = f[feature].keys()

    for feature in feature_list_toml:
        allele_ref_id = f['allele'][feature]['ref']
        if allele_ref_id not in allele_dict.keys():
            allele_dict.update({allele_ref_id: [alleles]})
        else:
                allele_dict.setdefault(allele_ref_id).append(alleles)


    for key in allele_dict:
        allele_dict[key].sort(key=len, reverse=True)


#%%
import toml
f = toml.load('../../data/alleles.toml')
fi = list(f.keys())
feature = fi[0]
print(feature)

# %%
