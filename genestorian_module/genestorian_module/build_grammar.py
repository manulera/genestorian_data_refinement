import json
import os
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))


def grammar_pattern_dict():
    ''''''
    with open(os.path.join(ROOT_DIR, "grammar", "pseudo_grammar.json")) as f:
        pseudo_grammar = json.load(f)
    # grammar_pattern_dict{pattern : [grammar rule name]}
    grammar_pattern_dict = {}
    for grammar in pseudo_grammar:
        grammar_dict = pseudo_grammar[grammar]
        if grammar_dict['pattern'] in grammar_pattern_dict:
            grammar_pattern_dict[grammar_dict['pattern']].append(grammar)
        else:
            grammar_pattern_dict[grammar_dict['pattern']] = [grammar]
    return grammar_pattern_dict


def build_grammar_rules():
    ''''''
    # grammar_dict{concatnated_chunk_rule_name : chunk_pattern}
    grammar_dict = {}
    grammar_rules = grammar_pattern_dict()
    for pattern_regex in grammar_rules:
        chunk_name = grammar_rules[pattern_regex][0]
        if len(grammar_rules[pattern_regex]) > 1:
            for i in range(len(grammar_rules[pattern_regex])-1):
                chunk_name += '|' + grammar_rules[pattern_regex][i+1]
        grammar_dict[chunk_name] = pattern_regex
    return grammar_dict


def grammar_dict_txt():
    grammar_dict = build_grammar_rules()
    with open(os.path.join(ROOT_DIR, "grammar", "grammar.txt"), 'w') as out:
        for grammar in grammar_dict:
            out.write(grammar + " : {" + grammar_dict[grammar] + "}\n")


if __name__ == "__main__":
    grammar_dict_txt()
