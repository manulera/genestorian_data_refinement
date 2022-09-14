
from nltk.tree import Tree
from nltk.chunk import RegexpParser
import json
import sys
import re
import warnings


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


def apply_chunker_match(matched_tree: Tree, pseudo_grammar):
    # For now we assume there can be no conflict between matches

    # The label contains the allele_features splitted by `|`
    match_label = matched_tree[0].label()

    # we return a copy if nothing is found
    out_tree = matched_tree.copy(deep=True)
    for allele_feature in match_label.split('|'):
        rule = pseudo_grammar[allele_feature]
        # If there are no rules that apply to 'other' features,
        # we automatically accept the match
        if len(rule['other_regex']) == 0:
            out_tree[0].set_label(allele_feature)
            return out_tree

        # In our grammar, the <other> tag cannot be optional we just assume '<other>' is always there for now
        other_tags = [tag for tag in matched_tree[0] if tag.label() == 'other']

        # TODO: this will fail if there are more than one <other> pattern, and not all are present.
        for regex, tag in zip(rule['other_regex'], other_tags):
            match = re.match(regex, tag[0])
            # All patterns must be matched
            if not match:
                return None
            # If the match does not span the entire thing
            if match.group() != tag[0]:
                # TODO handle this case
                warnings.warn(f'the tag {tag[0]} should be splitted')

        out_tree[0].set_label(allele_feature)
        return out_tree

    return None


def apply_pseudo_grammar(allele_tree, pseudo_grammar, chunker_list: list[RegexpParser]):
    for chunker in chunker_list:
        matched_tree: Tree = chunker.parse(allele_tree)
        # Match is found if the result is different
        if matched_tree != allele_tree:
            replaced_tree = apply_chunker_match(matched_tree, pseudo_grammar)
            # We found a match
            if replaced_tree:
                return replaced_tree

    # We didn't find anything
    return matched_tree


def main(input_file, pseudo_grammar_file, output_file):

    with open(pseudo_grammar_file) as f:
        pseudo_grammar = json.load(f)
    pattern2allele_features_dict = build_pattern2allele_features_dict(
        pseudo_grammar)
    chunker_list = create_chunker_list(pattern2allele_features_dict)
    allele_name2tree_dict = build_allele_name2tree_dict(input_file)

    trees_dict = {}
    for allele in allele_name2tree_dict:

        tree = apply_pseudo_grammar(
            allele_name2tree_dict[allele], pseudo_grammar, chunker_list)
        flat_tree = tree._pformat_flat("", "()", False)
        trees_dict[allele] = flat_tree

    with open(output_file, 'w', encoding="utf-8") as fp:
        json.dump(trees_dict, fp, indent=3, ensure_ascii=False)


if __name__ == "__main__":
    input_file = sys.argv[1]
    grammar_file = sys.argv[2]
    output_dir = sys.argv[3]
    main(input_file, grammar_file, output_dir)
