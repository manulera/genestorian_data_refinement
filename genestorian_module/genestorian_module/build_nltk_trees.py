
from ntpath import join
import re
from nltk.tree import Tree, ParentedTree
from nltk.chunk import RegexpParser
from genestorian_module.build_grammar import (build_grammar_rules,
                                              grammar_dict_txt)
import json
import os
import sys
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))


def build_tag_from_pattern(in_file):
    ''' Returns nltk input format to input into the parser

            Parameter:
                in_file :  alleles_pattern_nltk.json

            Return: 
                dict of allele tags in ntlk input
    '''
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
    '''
        Splits the value of other tag with respect to the match to he regex pattern 

        Parameters:
            other_tree_value(str) : value of other tree
            match(str) : str to reference the start and end co-ord to split

        Return:
            splitted_other_tree_value(list) : [elements of other_tree_value on splitting]
    '''
    start = other_tree_value.find(match[0])
    end = start + len(match)
    splitt_other_tree_value = [other_tree_value[:start],
                               other_tree_value[start:end], other_tree_value[end:]]

    return splitt_other_tree_value


def match_regex_pattern(other_tree, other_regex):
    '''
        Matches to regex pattern from pseudo_grammar

            Parameters:
                other_tree(nltk_tree): tree with label other
                other_regex(list): list of regex from pseudo_grammar

            Returns:
                match(str): other_regex match to other_tree value
                splitted_other_tree_value(list) : list of other_tree value splitted corresponding to the match
    '''
    splitted_other_tree_value = None
    for regex in other_regex:
        other_tree_value = other_tree[0]
        match = re.search(regex, other_tree_value)
        if match is not None:
            match = match.group(0)
            if match != other_tree_value:
                splitted_other_tree_value = split_other(
                    other_tree_value, match)

    return match, splitted_other_tree_value


def check_pseudo_grammar(rule_name_s, pseudo_grammar, other_tree):
    '''
        Returns the rule matched from the psudeo_grammar and splits the value 
        of the other tag in case the other_regex doesn't match to complete value

            Parameters: 
                rule_name_s (list): list of rule names 
                pseudo_grammar(dict) : dict of pseudo_grammar
                other_tree(nltk tree) : tree with other label in tree build by chunker

            Returns:
                matched_rule(str) : matched rule
                splitted_other_tree_value(list) : list of other value splitted 
    '''
    matched_rule = None
    for rule_name in rule_name_s:
        other_regex = pseudo_grammar[rule_name]['other_regex']
        if len(other_regex) != 0:
            match, splitted_other_tree_value = match_regex_pattern(
                other_tree, other_regex)
            if match is not None:
                matched_rule = rule_name
        else:
            matched_rule = rule_name
            splitted_other_tree_value = None
    return matched_rule, splitted_other_tree_value


def insert_to_tree(ptree, splitted_other_tree_value, other_tree):
    '''
        Inserts the splitted value of the other tag into the tree

            Parameters:
                tree(nltk tree): complete tree
                splitted_other_tree_value(list): splitted other tree value
                other_tree(nltk tree): tree with label other

            Returns:
                ptree(parented tree): tree with insertion of splitted_other_tree_value at target index
                  '''
    for s in ptree.subtrees(filter=lambda x: x.label() == 'other'):
        if other_tree[0] == s[0]:
            index = s.treeposition()
    # index of the split value is to determine the insert position in the tree
    ptree[index] = ParentedTree('other', [splitted_other_tree_value[1]])
    if splitted_other_tree_value[0] != '':
        ptree.insert(index[0], ParentedTree(
            'other', [splitted_other_tree_value[0]]))
    if splitted_other_tree_value[2] != '':
        ptree.insert(
            (index[0]+1), ParentedTree('other', [splitted_other_tree_value[2]]))
    return ptree


def delete_unmatched_tree(ptree):
    '''
        Deletes the subtree with rules that do not match the pattern in psuedo_grammar
        and inserts the nodes of the subtree back to the tree.

            Parameter:
                tree(nltk tree): tree

            Return:
                ptree(parented tree): tree with deleted subtree
        '''

    for s in ptree.subtrees(filter=lambda x: x.label() == ''):
        index_s = s.treeposition()
        # dict {(value , label) of nodes of the subtree to be deleted : index of the nodes}
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


def build_tag_from_tree(tree):
    '''
    Builds tag which can be input to the NLTK  RegexParser

        Parameter:
            tree(NLTK Tree): tree built by build_tree
        Return:
            Tag(Tree) : NLTK Regex Parser input  
    '''
    tag = []
    for i in range(len(tree)):
        value = []
        for j in range(len(tree[i])):
            value.append(tree[i][j])
        tag.append(Tree(tree[i].label(), value))
    return tag


def build_tree(grammar, allele, grammar_rule_dict, pseudo_grammar):
    '''Returns a tree which matches to the rule in peudo grammar

        Parameters:
            grammar(str): a rule to match 
            grammar_rule_dict: grammar_dict{concatnated_chunk_rule_name : pattern followed by the chunk}
            allele(Tree) : tagged allele features
            pseudo_grammar(dict): psuedo grammar dict

        Return:
            tree(nltk tree): tree with the matching pattern
    '''
    grammar = f""" {grammar}"""
    custom_tag_parser = RegexpParser(grammar)
    tree = custom_tag_parser.parse(allele)
    tree = ParentedTree.convert(tree)
    for s in tree.subtrees(lambda tree: tree.height() == 3):
        rule_name = s.label()
        if rule_name in grammar_rule_dict:
            rule_name_s = rule_name.split('|')
            for other_tree in s.subtrees(filter=lambda x: x.label() == 'other'):
                matched_rule, splitted_other_tree_value = check_pseudo_grammar(
                    rule_name_s, pseudo_grammar, other_tree)
                if splitted_other_tree_value is not None:
                    tree = insert_to_tree(
                        tree, splitted_other_tree_value, other_tree)
                if matched_rule is not None:
                    s.set_label(matched_rule)
                else:
                    s.set_label('')
                    tree = delete_unmatched_tree(tree)
    return tree


def recursive_build_tree(allele, grammars, counter,  grammar_rule_dict, pseudo_grammar):
    '''
    Recursively calls the build_tree until all the grammar rules are applied on the tree
        Parameters:
            allele(Tree) : tagged allele features
            grammars(str): a rules to match 
            counter(int): total number of grammars left to match
            grammar_rule_dict: grammar_dict{concatnated_chunk_rule_name : pattern followed by the chunk}
            pseudo_grammar(dict): psuedo grammar dict

        Return:
            tree(nltk tree): tree with all the patterns matched
        '''

    if counter > 1:
        grammar = grammars[counter-1].strip()
        tree = build_tree(grammar, allele, grammar_rule_dict, pseudo_grammar)
        tag = build_tag_from_tree(tree)
        return recursive_build_tree(tag, grammars, counter-1,  grammar_rule_dict, pseudo_grammar)
    else:
        return build_tree(grammars[0], allele, grammar_rule_dict, pseudo_grammar)

# def build_tree(custom_tag_parser, pseudo_grammar, grammar_rule_dict, allele):
#     '''
#         Returns a tree which matches to the rule in peudo grammar

#         Parameters:
#             custom_tag_parser(nltk parser):
#             pseudo_grammar(dict): psuedo grammar dict
#             grammar_rule_dict: grammar_dict{concatnated_chunk_rule_name : pattern followed by the chunk}
#             allele(tokenised text) : tokenised allele name

#         Return:
#             tree(nltk tree): tree with the matching patterns
#      '''
#     tree = custom_tag_parser.parse(allele)
#     tree = ParentedTree.convert(tree)
#     for s in tree.subtrees(lambda tree: tree.height() == 3):
#         rule_name = s.label()
#         if rule_name in grammar_rule_dict:
#             rule_name_s = rule_name.split('|')
#             for other_tree in s.subtrees(filter=lambda x: x.label() == 'other'):
#                 matched_rule, splitted_other_tree_value = check_pseudo_grammar(
#                     rule_name_s, pseudo_grammar, other_tree)
#                 if splitted_other_tree_value is not None:
#                     tree = insert_to_tree(
#                         tree, splitted_other_tree_value, other_tree)
#                 if matched_rule is not None:
#                     s.set_label(matched_rule)
#                 else:
#                     s.set_label('')
#                     tree = delete_unmatched_tree(tree)
#     return tree


def main(input_file):
    # makes sure to create a grammar.txt file
    grammar_dict_txt(os.path.join(ROOT_DIR, "grammar", "pseudo_grammar.json"))
    with open(os.path.join(ROOT_DIR, "grammar", "grammar.txt"), 'r') as fp:
        grammars = fp.readlines()
    with open(os.path.join(ROOT_DIR, "grammar", "pseudo_grammar.json")) as f:
        pseudo_grammar = json.load(f)
    grammar_rule_dict = build_grammar_rules(
        os.path.join(ROOT_DIR, "grammar", "pseudo_grammar.json"))
    allele_tags_dict = build_tag_from_pattern(input_file)

    # grammars = f""" {grammar}"""
    # custom_tag_parser = RegexpParser(grammar)
    trees_dict = {}
    for allele in allele_tags_dict:
        # tree = build_tree(custom_tag_parser, pseudo_grammar,
        #                   grammar_rule_dict, allele_tags_dict[allele])
        counter = len(grammars)
        tree = recursive_build_tree(
            allele_tags_dict[allele], grammars, counter,  grammar_rule_dict, pseudo_grammar)

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
