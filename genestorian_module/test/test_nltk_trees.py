import unittest
import os
import re
import json


class TestBuildNltkTrees(unittest.TestCase):
    def test_main(self):
        try:
            from genestorian_module.build_nltk_trees import main
        except ImportError:
            raise Exception(
                'main not imported from build_nltk_trees')

        output_file = main('./nltk_trees_dataset/alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./nltk_trees_dataset/nltk_trees.json'),
                        'nltk_trees.json not found')

        expected_output = {
            "ase1i130a,a143p": "(S (ALLELE_AA_SUBSTITUTION (GENE ase1) (other i130a,a143p)))",
            "pkj41x": "(S (other pkj41x))",
            "ase1-dummy-kanrother": "(S (dummy_matching_GENE_DELTION (GENE ase1) (- -) (other dummy) (- -) (MARKER kanr)) (other other))",
            "mph1δ::kanr": "(S (GENE_DELETION (GENE mph1) (other δ) (- ::) (MARKER kanr)))",
            "ase1(i130a,a143pap)": "(S (ALLELE_AA_SUBSTITUTION (GENE ase1) (other (i130a,a143p)) (other ap)))",
            "a-1pase1-ase1": "(S (other a) (- -) (other 1) (PROMOTER_GENE (other p) (GENE ase1) (- -) (GENE ase1)))"
        }
        with open('./nltk_trees_dataset/nltk_trees.json') as f:
            test_output = json.load(f)

        expected_output_sorted = sorted(expected_output.items())
        test_output_sorted = sorted(test_output.items())
        self.assertEqual(expected_output_sorted, test_output_sorted,
                         'output of main() is not as expected ')
