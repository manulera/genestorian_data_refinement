import json
from collections import Counter
import sys
import os


def build_common_pattern_dict(input_file):
    '''
    Builds a dictionary of common pattern followed by the the alleles

        Parameter:
            input_file(json): json file which has allele list 

        Returns:
            pattern_dict: dictionary{pattern: [alleles following pattern]}
    '''
    with open(input_file) as f:
        alleles_list = json.load(f)
    pattern_dict = {}
    for allele_dict in alleles_list:
        name = allele_dict['name']
        pattern = allele_dict['pattern']
        pattern_str = ''
        for element in pattern:
            if element[0] != 'other':
                pattern_str += element[0]
            else:
                pattern_str += element[1][0]
        if pattern_str in pattern_dict.keys():
            pattern_dict[pattern_str].append(name)
        else:
            pattern_dict[pattern_str] = [name]
    return pattern_dict


def json_common_pattern_dict(input_file):
    '''
    Saves the pattern_dict to a json file in the directory same a that of input_file

        Parameter"
            input_file(json): json file which has allele list 

        Return:
            None
    '''
    common_pattern_dict = build_common_pattern_dict(input_file)
    output_file = os.path.join(os.path.dirname(
        input_file), 'common_pattern.json')
    with open(output_file, 'w') as fp:
        json.dump(common_pattern_dict, fp, indent=3, ensure_ascii=False)


def count_common_patterns(input_file):
    '''
    Counts the number of alleles following the same pattern and writes it in
    a txt file in the same directory that of input_file.

        Parameters:
            input_file(json):json file which has allele list 

        Return:
            None
    '''
    occ_dict = build_common_pattern_dict(input_file)
    output_list = list()
    for key in occ_dict:
        output_list.append({'key': key, 'count': len(occ_dict[key])})
    output_list_sorted = sorted(
        output_list, key=lambda pattern: pattern['count'], reverse=True)
    output_file = os.path.join(os.path.dirname(
        input_file), 'common_pattern_count.txt')
    with open(output_file, 'w') as out:
        for pattern in output_list_sorted:
            out.write(f'{pattern["key"]}\t{pattern["count"]}\n')


def count_most_common_other_tag(input_file):
    '''Counts the frequency of unidentified elemens in the genotype and writes 
        in a txt file in the same directory that of input_file.

        Parameter:
            input_file(json):json file which has allele list 

        Return:
             None'''
    with open(input_file) as f:
        alleles_list = json.load(f)
    all_other_tag_list = list()
    for allele in alleles_list:
        for pattern in allele['pattern']:
            if pattern[0] == 'other':
                all_other_tag_list.append(pattern[1][0])
    counted_occurrences = Counter(all_other_tag_list).most_common()
    output_file = os.path.join(os.path.dirname(
        input_file), 'most_common_other_tag.txt')
    with open(output_file, 'w') as out:
        for occurrence, count in counted_occurrences:
            out.write(f'{occurrence}\t{count}\n')


def main(alleles_nltk_file):
    json_common_pattern_dict(alleles_nltk_file)
    count_common_patterns(alleles_nltk_file)
    count_most_common_other_tag(alleles_nltk_file)


if __name__ == "__main__":
    main(sys.argv[1])
