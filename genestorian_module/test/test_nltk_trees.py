from nltk import Tree
import unittest
import os
import json

class TestBuildNltkTrees(unittest.TestCase):
    def test_that_test_files_are_there(self):
        self.assertTrue(os.path.isfile('./nltk_trees_dataset/alleles_pattern_nltk.json'),
                        'The file alleles_pattern_nltk.json could not be found')

    def test_build_tag_from_pattern(self):
        try:
            from genestorian_module.build_nltk_trees import build_tag_from_pattern
        except ImportError:
            raise Exception(
                'build_tag_from_pattern not imported from build_nltk_trees')

        output = build_tag_from_pattern(
            './nltk_trees_dataset/alleles_pattern_nltk.json')

        self.assertEqual(type(output), dict,
                         'build_tag_from_pattern should return a dict')
        for key in output:
            self.assertEqual(type(output[key]), list,
                             'output dict key should be str and value should be list')

        expected_output = {'ase1i130a,a143p': [Tree('GENE', ['ase1']), Tree('other', ['i130a,a143p'])],
                           'pkj41x': [Tree('other', ['pkj41x'])],
                           'dummyase1-sad11other': [Tree('other', ['dummy']), Tree('GENE', ['ase1']),
                                                    Tree('-', ['-']), Tree('GENE', ['sad1']), Tree('other', ['1other'])],
                           'mph1δ::kanr': [Tree('GENE', ['mph1']), Tree('other', ['δ']), Tree('-', ['::']),
                                           Tree('MARKER', ['kanr'])],
                           'ase1(i130a,a143pap)': [Tree('GENE', ['ase1']), Tree('other', ['(i130a,a143pap)'])],
                           'a-1pase1-ase1': [Tree('other', ['a']), Tree('-', ['-']), Tree('other', ['1p']),
                                             Tree('GENE', ['ase1']), Tree('-', ['-']), Tree('GENE', ['ase1'])]}
        output_sorted = sorted(output.items())
        expected_output_sorted = sorted(expected_output.items())
        self.assertEqual(expected_output_sorted, output_sorted,
                         'input patterns are not tagged correctly ')

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
            "dummyase1-sad11other": "(S (dummy_matching_PROMOTER_GENE (other dummy) (GENE ase1) (- -) (GENE sad1)) (other 1other))",
            "mph1δ::kanr": "(S (GENE_DELETION (GENE mph1) (other δ) (- ::) (MARKER kanr)))",
            "ase1(i130a,a143pap)": "(S (ALLELE_AA_SUBSTITUTION (GENE ase1) (other (i130a,a143p)) (other ap)))",
            "a-1pase1-ase1": "(S (other a) (- -) (other 1) (PROMOTER_GENE (other p) (GENE ase1) (- -) (GENE ase1)))"
        }
        with open('./nltk_trees_dataset/nltk_trees.json') as f:
            test_output = json.load(f)

        expected_output_sorted = sorted(expected_output.items())
        test_output_sorted = sorted(test_output.items())
        self.assertEqual(expected_output_sorted, test_output_sorted,
                         'tree created by nltk chunker is not as expected')
