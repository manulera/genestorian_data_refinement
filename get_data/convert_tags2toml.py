# %%
import toml
import json
toml_dict = {'tag': dict()}

with open('tag_fpbase.json') as f:
    tags_list = json.load(f)
for tag in tags_list:
    if tag['aliases'] is not None:
        toml_dict['tag'][tag['name']] = {
            'name': tag['name'],
            'reference': tag['reference'],
            'synonyms': tag['aliases']
        }
        if len(toml_dict['tag'][tag['name']]['synonyms']) == 0:
            toml_dict['tag'][tag['name']].pop('synonyms')

    else:
        toml_dict['tag'][tag['name']] = {
            'name': tag['name'],
            'reference': tag['reference']
        }

    if len(toml_dict['tag'][tag['name']]['reference']) == 0:
        toml_dict['tag'][tag['name']].pop('reference')

with open('../allele_components/tags_fpbase.toml', "w") as toml_file:
    toml.dump(toml_dict, toml_file)

