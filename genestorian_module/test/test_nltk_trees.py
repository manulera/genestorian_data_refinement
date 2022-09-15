import unittest
import os
import json

class TestBuildNltkTrees(unittest.TestCase):
    def test_that_test_files_are_there(self):
        self.assertTrue(os.path.isfile('./nltk_trees_dataset/alleles_pattern_nltk.json'),
                        'The file alleles_pattern_nltk.json could not be found')

    def test_build_tag_from_pattern(self):
        try:
            from genestorian_module.build_nltk_trees import build_allele_name2tree_dict
        except ImportError:
            raise Exception(
                'build_allele_name2tree_dict not imported from build_nltk_trees')

        output = build_allele_name2tree_dict(
            './nltk_trees_dataset/alleles_pattern_nltk.json')

        self.assertEqual(type(output), dict,
                         'build_allele_name2tree_dict should return a dict')

    def test_main(self):
        try:
            from genestorian_module.build_nltk_trees import main
        except ImportError:
            raise Exception(
                'main not imported from build_nltk_trees')

        main('./nltk_trees_dataset/alleles_pattern_nltk.json', './nltk_trees_dataset/pseudo_grammar.json', './nltk_trees_dataset/nltk_trees.json')
        self.assertTrue(os.path.isfile('./nltk_trees_dataset/nltk_trees.json'),
                        'nltk_trees.json not found')

        expected_output = {
            "ase1i130a,a143p": "(ROOT (ALLELE_AA_SUBSTITUTION (GENE ase1) (other i130a,a143p)))",
            "pkj41x": "(ROOT (other pkj41x))",
            "dummyase1-sad11other": "(ROOT (dummy_matching_PROMOTER_GENE (other dummy) (GENE ase1)) (- -) (GENE sad1) (other 1other))",
            "mph1δ::kanr": "(ROOT (GENE_DELETION (GENE mph1) (other δ) (- ::) (MARKER kanr)))",
            "ase1(i130a,a143pap)": "(ROOT (ALLELE_AA_SUBSTITUTION (GENE ase1) (other (i130a,a143p)) (other ap)))",
            "a-1pase1-ase1": "(ROOT (other a) (- -) (other 1) (PROMOTER_GENE (other p) (GENE ase1)) (- -) (GENE ase1))"
        }
        with open('./nltk_trees_dataset/nltk_trees.json') as f:
            test_output = json.load(f)

        expected_output_sorted = sorted(expected_output.items())
        test_output_sorted = sorted(test_output.items())
        self.assertEqual(expected_output_sorted, test_output_sorted,
                         'tree created by nltk chunker is not as expected')
