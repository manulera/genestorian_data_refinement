# %%
import json

with open('occurences2.json') as ins:
    occ_dict = json.load(ins)

results_list = list()
for key in occ_dict:
    results_list.append({'key': key, 'count': len(occ_dict[key])})

results_sorted = sorted(
    results_list, key=lambda pattern: pattern['count'], reverse=True)

with open('summary_occurences.txt', 'w') as out:
    for result in results_sorted:
        out.write(f'{result["key"]}\t{result["count"]}\n')
