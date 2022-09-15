

from copy import deepcopy
from nltk.tree import ParentedTree
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


def replace_parentedtree_node(tree: ParentedTree, target_node: ParentedTree, insert_nodes, inplace=True):
    '''
    Return a COPY of a ParentedTree with a given node replaced by several, or replace if inplace is True
    nodes, passed in insert_nodes
    '''
    insertion_index = target_node.parent_index()
    if not inplace:
        tree = tree.copy(deep=True)
    tree.remove(target_node)
    for ele in insert_nodes[::-1]:
        tree.insert(insertion_index, ele)
    return tree


def check_regex_match(matched_subtree: ParentedTree, other_regex_patterns):
    '''
    Tests the regex in rule['other_regex'], three possible outcomes:
        - 'no match': regex not satisfied, so keep going
        - 'match': regex is matched, and matches the entire <other> tag
        - 'split parent': regex is found, but does not match the entire <other>
          tag, so the tag has to be splitted, second return value is a list with
          a list of trees after the split, that should be used to replace the
          matched_subtree
    '''
    # Get the trees from <other> tags.
    other_trees = [sstree for sstree in matched_subtree
                   if sstree.label() == 'other']

    for regex, other_tree in zip(other_regex_patterns, other_trees):
        other_tree: ParentedTree
        match: re.Match[str] = re.search(regex, other_tree[0])
        if not match:
            return 'no match', []
        if match.group() != other_tree[0]:
            # Partition is a string method like split, but preserves the delimiter. the `if substr` is to remove
            # the empty string: e.g., 'helloworld'.partition('hello') -> ['','hello','world']
            trees4replacement = [ParentedTree(
                'other', [substr]) for substr in other_tree[0].partition(match.group()) if substr]
            # return a list of trees to replace matched_subtree in the parent,
            # and restart the rule application from the current rule again
            output_tree = replace_parentedtree_node(
                matched_subtree, other_tree, trees4replacement)
            return 'split parent', [t.copy(deep=True) for t in output_tree]

    # No errors in matching
    return 'match', []


def apply_pseudo_grammar(allele_tree: ParentedTree, pseudo_grammar):
    output_tree = allele_tree.copy(deep=True)

    for rule_i, rule in enumerate(pseudo_grammar):
        parser: RegexpParser = rule['parser']
        updated_tree: ParentedTree = ParentedTree.convert(
            parser.parse(output_tree))
        # Match is found if the result is different
        if updated_tree != output_tree:
            other_regex_patterns = rule['other_regex']
            if len(other_regex_patterns) == 0:
                # No rules for <other>, we have a match
                output_tree = updated_tree
                continue

            # we have to make sure that regex patterns are matched,
            # and splitted if needed
            for matched_subtree in updated_tree.subtrees(filter=lambda x: x.label() == rule['feature_name']):
                outcome, matched_subtree_replacement = check_regex_match(
                    matched_subtree, other_regex_patterns)
                if outcome == 'no match':
                    replace_parentedtree_node(updated_tree, matched_subtree, [
                                              t.copy(deep=True) for t in matched_subtree], True)
                elif outcome == 'split parent':
                    output_tree = replace_parentedtree_node(
                        updated_tree, matched_subtree, matched_subtree_replacement)
                    # We apply the same rule again (there might be further splits to do, or the same thing twice)
                    return apply_pseudo_grammar(output_tree, pseudo_grammar[rule_i:])
            else:
                output_tree = updated_tree

    return output_tree


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
