

from copy import deepcopy
from nltk.tree import Tree
import json
import sys
import re
import warnings
from nltk.chunk import RegexpParser


def post_process_pseudo_grammar(pseudo_grammar: dict):
    out_grammar = deepcopy(pseudo_grammar)
    for rule in out_grammar:
        rule['parser'] = RegexpParser(
            f'{rule["feature_name"]}: ' + '{' + rule['pattern'] + '}',
            root_label='ROOT')
    return out_grammar


def build_allele_name2tree_dict(in_file):
    ''' Returns nltk input format to input into the parser

            Parameter:
                in_file :  alleles_pattern_nltk.json

            Return:
                dict of allele tags in ntlk input
    '''
    with open(in_file) as fp:
        allele_list = json.load(fp)
    allele_name2tree_dict = {}
    for allele in allele_list:
        tree_list = []
        allele_name = allele['name']
        patterns = allele['pattern']
        for pattern in patterns:
            tree_list.append(Tree(pattern[0], pattern[1]))
        # We create a root element called ALLELE
        allele_name2tree_dict[allele_name] = Tree('ROOT', tree_list)
    return allele_name2tree_dict


def apply_pseudo_grammar(allele_tree, pseudo_grammar):

    for rule in pseudo_grammar:
        parser: RegexpParser = rule['parser']
        matched_tree: Tree = parser.parse(allele_tree)
        # Match is found if the result is different
        if matched_tree != allele_tree:
            other_regex_patterns = rule['other_regex']
            if len(other_regex_patterns) == 0:
                # No rules for <other>, we have a match
                return matched_tree

            other_tags = [tag for tag in matched_tree[0]
                          if tag.label() == 'other']
            # We check for the <other> rules
            for regex, tag in zip(other_regex_patterns, other_tags):
                match = re.match(regex, tag[0])
                if not match:
                    break
                if match.group() != tag[0]:
                    # TODO handle this case
                    warnings.warn(f'the tag {tag[0]} should be splitted')
            else:
                # Return the match if no breaks
                return matched_tree

    return allele_tree


def main(input_file, pseudo_grammar_file, output_file):

    with open(pseudo_grammar_file) as f:
        pseudo_grammar = json.load(f)
    pseudo_grammar = post_process_pseudo_grammar(pseudo_grammar)
    allele_name2tree_dict = build_allele_name2tree_dict(input_file)

    trees_dict = {}
    for allele in allele_name2tree_dict:

        tree = apply_pseudo_grammar(
            allele_name2tree_dict[allele], pseudo_grammar)
        flat_tree = tree._pformat_flat("", "()", False)
        trees_dict[allele] = flat_tree

    with open(output_file, 'w', encoding="utf-8") as fp:
        json.dump(trees_dict, fp, indent=3, ensure_ascii=False)


if __name__ == "__main__":
    input_file = sys.argv[1]
    grammar_file = sys.argv[2]
    output_dir = sys.argv[3]
    main(input_file, grammar_file, output_dir)
