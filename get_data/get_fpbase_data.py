# %%
import toml
import requests
import json


query = """{
  allProteins(name_Icontains:""){
    edges{
      node{
        name,
        aliases,
        primaryReference{
          doi
        }
      }
    }
  }
}"""
url = 'https://www.fpbase.org/graphql/'
r = requests.post(url, json={'query': query})
json_data = json.loads(r.text)


node_list = json_data['data']['allProteins']['edges']
tags_list = []
for node in node_list:
    tags_list.append(node['node'])
for tag in tags_list:
    if tag['primaryReference'] is not None:
        tag["reference"] = tag['primaryReference']["doi"]
        tag = tag.pop('primaryReference')
    else:
        tag['reference'] = ''
        tag = tag.pop('primaryReference')

toml_dict = {'tag': dict()}

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

# %%
