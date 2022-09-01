# %%
from ntpath import join
import re
from nltk.tree import Tree, ParentedTree
from nltk.chunk import RegexpParser
from genestorian_module.build_grammar import build_grammar_rules
import json
import os
import sys
# %%


def build_tag_from_pattern(in_file):
    with open(in_file) as fp:
        allele_list = json.load(fp)
    allele_tags_dict = {}
    for allele in allele_list:
        tag = []
        allele_name = allele['name']
        patterns = allele['pattern']
        for pattern in patterns:
            tag.append(Tree(pattern[0], pattern[1]))
        allele_tags_dict[allele_name] = tag
    return allele_tags_dict


def split_other(other_tree_value, match):
    start = other_tree_value.find(match[0])
    end = start + len(match)
    split_other_tree_value = [other_tree_value[:start],
                              other_tree_value[start:end], other_tree_value[end:]]

    return split_other_tree_value


def match_regex_pattern(other_tree, other_regex):
    split_other_tree_value = None
    for regex in other_regex:
        other_tree_value = other_tree[0]
        match = re.search(regex, other_tree_value)
        if match is not None:
            match = match.group(0)
            if match != other_tree_value:
                split_other_tree_value = split_other(
                    other_tree_value, match)

    return match, split_other_tree_value


def check_pseudo_grammar(rule_name_s, pseudo_grammar, other_tree):
    matched_rule = None
    for rule_name in rule_name_s:
        other_regex = pseudo_grammar[rule_name]['other_regex']
        if len(other_regex) != 0:
            match, split_other_tree_value = match_regex_pattern(
                other_tree, other_regex)
            if match is not None:
                matched_rule = rule_name
        else:
            matched_rule = rule_name
            split_other_tree_value = None
    return matched_rule, split_other_tree_value


def insert_to_tree(tree, addition_to_tree, other_tree):
    ptree = ParentedTree.convert(tree)
    for s in ptree.subtrees(filter=lambda x: x.label() == 'other'):
        if other_tree[0] == s[0]:
            index = s.treeposition()
    ptree[index] = ParentedTree('other', [addition_to_tree[1]])
    if addition_to_tree[0] != '':
        ptree.insert(index[0], ParentedTree('other', [addition_to_tree[0]]))
    if addition_to_tree[2] != '':
        ptree.insert(
            (index[0]+1), ParentedTree('other', [addition_to_tree[2]]))
    return ptree


def delete_unmatched_tree(tree):
    ptree = ParentedTree.convert(tree)
    for s in ptree.subtrees(filter=lambda x: x.label() == ''):
        index_s = s.treeposition()
        dict_subtree_s = {}
        for subtree_s in s.subtrees():
            index_subtree_s = subtree_s.treeposition()
            if len(index_subtree_s) > 1:
                tag_label = str(subtree_s.label())
                tag_value = str(subtree_s[0])
                key = (tag_value, tag_label)
                dict_subtree_s[key] = index_subtree_s

    ptree.pop(index_s[0])

    for key in dict_subtree_s:
        index = dict_subtree_s[key]
        ptree.insert(index[0]+index[1],
                     ParentedTree(key[1], [key[0]]))
    return ptree


def build_tree(custom_tag_parser, pseudo_grammar, grammar_rule_dict, tag):

    tree = custom_tag_parser.parse(tag)
    for s in tree.subtrees(lambda tree: tree.height() == 3):
        rule_name = s.label()
        if rule_name in grammar_rule_dict:
            rule_name_s = rule_name.split('|')
            for other_tree in s.subtrees(filter=lambda x: x.label() == 'other'):
                matched_rule, addition_to_tree = check_pseudo_grammar(
                    rule_name_s, pseudo_grammar, other_tree)
                if addition_to_tree is not None:
                    tree = insert_to_tree(tree, addition_to_tree, other_tree)
                if matched_rule is not None:
                    s.set_label(matched_rule)
                else:
                    s.set_label('')
                    tree = delete_unmatched_tree(tree)
    return tree


def main(input_file):
    with open('./grammar/grammar.txt', 'r') as fp:
        grammar = fp.read().strip()
    with open('./grammar/pseudo_grammar.json') as f:
        pseudo_grammar = json.load(f)
    grammar_rule_dict = build_grammar_rules()
    allele_tags_dict = build_tag_from_pattern(input_file)

    grammar = f""" {grammar}"""
    custom_tag_parser = RegexpParser(grammar)
    trees_dict = {}
    for allele in allele_tags_dict:
        tree = build_tree(custom_tag_parser, pseudo_grammar,
                          grammar_rule_dict, allele_tags_dict[allele])
        flat_tree = tree._pformat_flat("", "()", False)

        trees_dict[allele] = flat_tree
    output_file_name = 'nltk_trees.json'
    output_dir = os.path.dirname(input_file)
    output_file_path = os.path.join(output_dir, output_file_name)

    with open(output_file_path, 'w', encoding="utf-8") as fp:
        json.dump(trees_dict, fp, indent=3, ensure_ascii=False)
    return None


if __name__ == "__main__":
    input_file = sys.argv[1]
    main(input_file)


# %%
