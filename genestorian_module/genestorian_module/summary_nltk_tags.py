import json
import re
from collections import Counter
import pandas as pd
import sys, os

def build_common_pattern_dict(input_file):
    with open(input_file) as f:
        alleles_list = json.load(f)
    pattern_dict = {}
    for allele_dict in alleles_list:
        name = allele_dict['name']
        pattern = allele_dict['pattern']
        pattern_str = ''
        for element in pattern:
            if element[1] != 'other':
                pattern_str += element[1]
            else:
                pattern_str += element[0]
        if pattern_str in pattern_dict.keys():
            pattern_dict[pattern_str].append(name)
        else:
            pattern_dict[pattern_str] = [name]
    return pattern_dict


def json_common_pattern_dict(input_file):
    common_pattern_dict = build_common_pattern_dict(input_file)
    output_file = os.path.join(os.path.dirname(input_file), 'common_pattern.json')
    with open(output_file, 'w') as fp:
        json.dump(common_pattern_dict, fp, indent=3, ensure_ascii=False)


def count_common_patterns(input_file):
    occ_dict = build_common_pattern_dict(input_file)
    output_list = list()
    for key in occ_dict:
        output_list.append({'key': key, 'count': len(occ_dict[key])})
    output_list_sorted = sorted(
        output_list, key=lambda pattern: pattern['count'], reverse=True)
    output_file = os.path.join(os.path.dirname(input_file), 'common_pattern_count.txt')
    with open(output_file, 'w') as out:
        for pattern in output_list_sorted:
            out.write(f'{pattern["key"]}\t{pattern["count"]}\n')


def count_most_common_other_tag(input_file):
    occ_dict = build_common_pattern_dict(input_file)
    result_list = []
    for key in occ_dict:
        split_elements = re.split(
            r'ALLELE|GENE|TAG|MARKER|PROMOTER|-', key)
        result_list = result_list + split_elements*len(occ_dict[key])
    df_unidentified_feature_occurences = pd.DataFrame(Counter(result_list).items(), columns=[
        'feature', 'no_of_occurence'])
    df_unidentified_feature_occurences = df_unidentified_feature_occurences.sort_values(
        'no_of_occurence', ascending=False)
    output_file = os.path.join(os.path.dirname(input_file), 'most_common_other_tag.tsv')
    df_unidentified_feature_occurences.to_csv(output_file, sep='\t', index=False)



def main(alleles_nltk_file):
    json_common_pattern_dict(alleles_nltk_file)
    count_common_patterns(alleles_nltk_file)
    count_most_common_other_tag(alleles_nltk_file)


if __name__ == "__main__":
    main(sys.argv[1])
