# %%
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


with open('tag_fpbase.json', 'w', encoding="utf-8") as fp:
    json.dump(tags_list, fp, indent=3, ensure_ascii=False)

# %%
