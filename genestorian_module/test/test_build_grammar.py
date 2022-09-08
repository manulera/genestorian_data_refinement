from genericpath import isfile
import unittest


class TestBuildNltkTags(unittest.TestCase):
    def test_input_file_is_present(self):
        self.assertTrue(isfile('./nltk_trees_dataset/pseudo_grammar.json'),
                        'File pseudo_grammar.json not found')

    def test_grammar_pattern_dict(self):
        try:
            from genestorian_module.build_grammar import grammar_pattern_dict
        except ImportError:
            raise Exception(
                'grammar_pattern_dict not imported from build_grammar')
        grammar_pattern_dict = grammar_pattern_dict(
            './nltk_trees_dataset/pseudo_grammar.json')
        self.assertEqual(type(grammar_pattern_dict), dict,
                         'The output of grammar_pattern_dict should be a dictionary ')
        for pattern in grammar_pattern_dict:
            self.assertEqual(type(grammar_pattern_dict[pattern]), list,
                             'The value of keys in  grammar_pattern_dict should be list of rule names')
        expected_grammar_pattern_dict = {'<GENE><->?<other>?<->?<MARKER>': ['GENE_DELETION'],
                                         '<other><GENE><-><GENE>': ['dummy_matching_PROMOTER_GENE', 'PROMOTER_GENE'],
                                         '<GENE><->?<other>': ['ALLELE_AA_SUBSTITUTION'],
                                         '<GENE><->?<TAG><->?<MARKER>': ['C_Terminal_Tagging']}

        sorted_grammar_pattern_dict = sorted(grammar_pattern_dict.items())
        sorted_expected_grammar_pattern_dict = sorted(
            expected_grammar_pattern_dict.items())
        self.assertEqual(sorted_expected_grammar_pattern_dict, sorted_grammar_pattern_dict,
                         'grammar_pattern_dict output not as expected')

    def test_build_grammar_rules(self):
        try:
            from genestorian_module.build_grammar import build_grammar_rules
        except ImportError:
            raise Exception(
                'build_grammar_rules not imported from build_grammar')
        grammar_rules = build_grammar_rules(
            './nltk_trees_dataset/pseudo_grammar.json')
        self.assertEqual(type(grammar_rules), dict,
                         'The output of build_grammar_rules should be a dictionary ')
        for rule in grammar_rules:
            self.assertEqual(type(grammar_rules[rule]), str,
                             'The value of keys in  grammar_rules should be string of pattern')

        expected_grammar_rules = {'GENE_DELETION': '<GENE><->?<other>?<->?<MARKER>',
                                  'dummy_matching_PROMOTER_GENE|PROMOTER_GENE': '<other><GENE><-><GENE>',
                                  'ALLELE_AA_SUBSTITUTION': '<GENE><->?<other>',
                                  'C_Terminal_Tagging': '<GENE><->?<TAG><->?<MARKER>'}

        expected_grammar_rules_sorted = sorted(expected_grammar_rules.items())
        grammar_rules_sorted = sorted(grammar_rules.items())
        self.assertEqual(expected_grammar_rules_sorted, grammar_rules_sorted,
                         'grammar_rules output not as expected')

    def test_grammar_dict_txt(self):
        try:
            from genestorian_module.build_grammar import grammar_dict_txt
        except ImportError:
            raise Exception(
                'grammar_dict_txt not imported from build_grammar')
        grammar_dict_txt('./nltk_trees_dataset/pseudo_grammar.json')
        self.assertTrue(isfile('./nltk_trees_dataset/pseudo_grammar.json'),
                        'File pseudo_grammar.json not found')
