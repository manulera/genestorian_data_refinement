# %%
from ntpath import join
import re
from nltk.tree import Tree
from nltk.chunk import RegexpParser

pseudo_grammar = {
    'GENE_DELETION': {
        'pattern': '<GENE><SPACER>?<other>?<SPACER>?<MARKER>',
        'other_regex': ['^(delta|δ)$']
    },
    'hallo': {
        'pattern': '<GENE><SPACER>?<other>?<SPACER>?<MARKER>',
        'other_regex': ['^(hallo)$']
    },
    'blah': {
        'pattern': '<other><SPACER>?<other>?<SPACER>?<MARKER>',
        'other_regex': ['^(blah)$']
    }
}


def dict_grammar_rules(pseudo_grammar):
    grammar_rules = {}
    for key in pseudo_grammar:
        if pseudo_grammar[key]['pattern'] in grammar_rules:
            grammar_rules[pseudo_grammar[key]['pattern']].append(key)
        else:
            grammar_rules[pseudo_grammar[key]['pattern']] = [key]
    return grammar_rules


def build_grammar_dict(grammar_rules):
    grammar = {}
    for pattern_regex in grammar_rules:
        chunk_name = grammar_rules[pattern_regex][0]
        if len(grammar_rules[pattern_regex]) > 1:
            for i in range(len(grammar_rules[pattern_regex])-1):
                chunk_name += '*' + grammar_rules[pattern_regex][i+1]
        grammar[chunk_name] = pattern_regex
    return grammar


def convert_grammar_dict(grammar_dict):
    with open('dummy_grammar.txt', 'w') as out:
        for grammar in grammar_dict:
            out.write(grammar + " : {" + grammar_dict[grammar] + "}\n")


grammar_rules = dict_grammar_rules(pseudo_grammar)
grammar_dict = build_grammar_dict(grammar_rules)
convert_grammar_dict(grammar_dict)
# %%


def match_regex_pattern(other_tree, other_regex):
    for regex in other_regex:
        other_tree_value = other_tree[0]
        match = re.match(regex, other_tree_value)
    return match


def check_pseudo_grammar(rule_name_s, pseudo_grammar, other_tree):
    matched_rule = []
    for rule_name in rule_name_s:
        other_regex = pseudo_grammar[rule_name]['other_regex']
        matches = match_regex_pattern(other_tree, other_regex)
        if matches is not None:
            matched_rule.append(rule_name)
    return matched_rule


# %%
with open('dummy_grammar.txt', 'r') as fp:
    grammer = fp.read().strip()
grammar = f""" {grammer}"""


tags = [[
    Tree('GENE', ['ase1']),
    Tree('other', ['a']),
    Tree('SPACER', ['-']),
    Tree('MARKER', ['kanr']),
    Tree('other', ['abc'])],
    [
    Tree('GENE', ['mph1']),
    Tree('other', ['δ']),
    Tree('SPACER', ['::']),
    Tree('MARKER', ['kanr']),
],
    [
    Tree('other', ['pkj41x']),
]
]
custom_tag_parser = RegexpParser(grammar)


# for tag in tags:
#     custom_tag_parser = RegexpParser(grammar)
#     tree = custom_tag_parser.parse(tag)
#     for subtree in tree.subtrees():
#         rule_name = subtree.label()
#         if rule_name in grammar_dict:
#             rule_name_s = re.split('\*', rule_name)
#             for other_tree in subtree.subtrees(filter=lambda x: x.label() == 'other'):
#                 matched_rule = check_pseudo_grammar(
#                     rule_name_s, pseudo_grammar, other_tree)
#                 if len(matched_rule) != 0:
#                     flat_tree = tree._pformat_flat("", "()", False)
#                     flat_tree = flat_tree.replace(rule_name, matched_rule[0])
#                 else:
#                     flat_tree = tree._pformat_flat("", "()", False)
#                 print(flat_tree)

# %%
for tag in tags:
    tree = custom_tag_parser.parse(tag)
    for s in tree.subtrees(lambda tree: tree.height() == 3):
        rule_name = s.label()
        if rule_name in grammar_dict:
            rule_name_s = re.split('\*', rule_name)
            for other_tree in s.subtrees(filter=lambda x: x.label() == 'other'):
                matched_rule = check_pseudo_grammar(
                    rule_name_s, pseudo_grammar, other_tree)
                if len(matched_rule) != 0:
                    s.set_label(matched_rule[0])

    print(s)

# %%
