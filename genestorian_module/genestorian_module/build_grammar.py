import json
import sys
from nltk.chunk import RegexpParser


def build_pattern2allele_features_dict(pseudo_grammar):
    pattern2allele_features_dict = dict()
    for allele_feature in pseudo_grammar:
        rule = pseudo_grammar[allele_feature]
        if rule['pattern'] in pattern2allele_features_dict:
            pattern2allele_features_dict[rule['pattern']].append(
                allele_feature)
        else:
            pattern2allele_features_dict[rule['pattern']] = [allele_feature]
    return pattern2allele_features_dict


def create_chunker_list(pattern2allele_features_dict) -> list[RegexpParser]:
    '''
    Build a list in which each element is a chunker generated from one of the rules
    '''
    out = list()
    for pattern, allele_features in pattern2allele_features_dict.items():
        out.append(RegexpParser(
            '|'.join(allele_features) + ' : {' + pattern + '}\n',
            root_label='ROOT'),)
    return out

# The `main` function is not necessary, but it can be nice to print that grammar.txt
# to double check


def main(input_file, output_file):

    with open(input_file) as f:
        pseudo_grammar = json.load(f)

    pattern2allele_features_dict = build_pattern2allele_features_dict(
        pseudo_grammar)

    with open(output_file, 'w') as out:
        for pattern, allele_features in pattern2allele_features_dict.items():
            out.write('|'.join(allele_features) + ' : {' + pattern + '}\n')


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
