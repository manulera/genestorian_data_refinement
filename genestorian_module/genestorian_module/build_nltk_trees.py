

from copy import deepcopy
from nltk.tree import ParentedTree, Tree
import json
import sys
import re

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
            tree_list.append(ParentedTree(pattern[0], pattern[1]))
        # We create a root element called ALLELE
        allele_name2tree_dict[allele_name] = ParentedTree('ROOT', tree_list)
    return allele_name2tree_dict


def apply_regex_rule(matched_subtree: ParentedTree, other_regex_patterns):

    other_trees = [sstree for sstree in matched_subtree
                   if sstree.label() == 'other']

    for regex, other_tree in zip(other_regex_patterns, other_trees):
        other_tree: ParentedTree
        match: re.Match[str] = re.search(regex, other_tree[0])
        if not match:
            break
        if match.group() != other_tree[0]:
            start, end = match.span()
            other_str = other_tree[0]
            this_list = [other_str[:start],
                         other_str[start:end], other_str[end:]]
            this_list = list(filter(lambda x: x != '', this_list))
            insertion_index = other_tree.parent_index()
            matched_subtree.remove(other_tree)
            for ele in this_list:
                matched_subtree.insert(
                    insertion_index, ParentedTree('other', [ele]))
            print(matched_subtree[:])
            # return apply_pseudo_grammar(ParentedTree('ROOT', tree_list), [rule])
    # else:
    #     # Return the match only if no break
    #     return 1


def apply_pseudo_grammar(allele_tree: ParentedTree, pseudo_grammar):

    output_tree = allele_tree.copy(deep=True)

    for rule in pseudo_grammar:
        parser: RegexpParser = rule['parser']
        updated_tree: ParentedTree = ParentedTree.convert(
            parser.parse(output_tree))
        # Match is found if the result is different
        if updated_tree != allele_tree:
            other_regex_patterns = rule['other_regex']
            if len(other_regex_patterns) == 0:
                # No rules for <other>, we have a match
                output_tree = updated_tree
                continue

            # we have to make sure that regex patterns are matched, and split if needed
            for matched_subtree in updated_tree.subtrees(filter=lambda x: x.label() == rule['feature_name']):
                apply_regex_rule(matched_subtree, other_regex_patterns)

            # # We store the index of the tags that correspond to <other> elements
            # other_tag_indexes = [tag_i for tag_i, tag in enumerate(updated_tree[0])
            #                      if tag.label() == 'other']
            # # We check for the <other> rules
            # for regex, tag_i in zip(other_regex_patterns, other_tag_indexes):
            #     tag = updated_tree[0][tag_i]
            #     match: re.Match[str] = re.search(regex, tag[0])
            #     if not match:
            #         break
            #     if match.group() != tag[0]:
            #         start, end = match.span()
            #         other_str = tag[0]
            #         this_list = [other_str[:start],
            #                      other_str[start:end], other_str[end:]]
            #         this_list = list(filter(lambda x: x != '', this_list))
            #         new_trees = [ParentedTree('other', [ele]) for ele in this_list]
            #         tree_list = updated_tree[0][:tag_i] + \
            #             new_trees + updated_tree[0][tag_i+1:]
            #         print(allele_tree)
            #         print(ParentedTree('ROOT', tree_list))
            #         return apply_pseudo_grammar(ParentedTree('ROOT', tree_list), [rule])
            # else:
            #     # Return the match only if no break
            #     return updated_tree

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
