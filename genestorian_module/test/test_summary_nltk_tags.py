import unittest
import os
import re


class TestSummaryNltkTags(unittest.TestCase):
    def input_file_is_present(self):
        self.assertTrue(os.path.isfile('./alleles_pattern_nltk.json'),
                        'The file alleles_nltk.json not found')

    def test_build_common_pattern_dict(self):
        try:
            from genestorian_module.summary_nltk_tags import build_common_pattern_dict
        except ImportError:
            raise Exception(
                'build_common_pattern_dict not imported from summary_nltk_tags')
        pattern_dict = build_common_pattern_dict('./alleles_pattern_nltk.json')
        pattern_dict_keys = ['ALLELE/ALLELE',
                             'GENEδ-MARKER', 'TAG0/TAG0', 'GENE-1/GENE-1', '+/GENE', 'ALLELE', 'GENE/+']
        self.assertEqual(type(pattern_dict), dict,
                         'Output of test_build_common_pattern_dict should be a dict')
        self.assertEqual(len(pattern_dict.keys()), len(pattern_dict_keys),
                         'pattern_dict keys do not match the sample list')
        for i in range(len(pattern_dict_keys)):
            self.assertTrue(pattern_dict_keys[i] in list(
                pattern_dict.keys()), 'list not equal')

    def test_json_common_pattern_dict(self):
        try:
            from genestorian_module.summary_nltk_tags import json_common_pattern_dict
        except ImportError:
            raise Exception(
                'json_common_pattern_dict not imported from summary_nltk_tags')
        json_file = json_common_pattern_dict('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./common_pattern.json'),
                        'json_common_pattern_dict did not produce any json file')

    def test_count_common_patterns(self):
        try:
            from genestorian_module.summary_nltk_tags import count_common_patterns
        except ImportError:
            raise Exception(
                'count_common_patterns not imported from summary_nltk_tags')
        try:
            from genestorian_module.summary_nltk_tags import build_common_pattern_dict
        except ImportError:
            raise Exception(
                'build_common_pattern_dict not imported from summary_nltk_tags')
        txt_file = count_common_patterns('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./common_pattern_count.txt'),
                        'count_common_patterns did not produce any txt file')
        pattern_dict = build_common_pattern_dict('./alleles_pattern_nltk.json')
        total_num_of_patterns = len(list(pattern_dict.keys()))
        with open('common_pattern_count.txt', 'r') as f:
            total_num_patterns_file = len(f.readlines())
        self.assertEqual(total_num_patterns_file,
                         total_num_of_patterns, 'all patterns are not counted')

    def test_count_most_common_other_tag(self):
        try:
            from genestorian_module.summary_nltk_tags import count_most_common_other_tag
        except ImportError:
            raise Exception(
                'count_most_common_other_tag not imported from summary_nltk_tags')
        tsv_file = count_most_common_other_tag('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./most_common_other_tag.tsv'),
                        'count_common_patterns did not produce any tsv file')
