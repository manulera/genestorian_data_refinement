import unittest
import os
import json
from collections import OrderedDict


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
        pattern_dict_test = {
            "GENE-MARKER": ["mug28::kanmx6"],
            "ALLELE": ["ade6-m216", "ura4-"],
            "GENE+-laci-TAG": ["his7+::laci-gfp"],
            "ALLELE-laco": ["lys1+::laco"],
            "GENE9-MARKER": ["mug29::kanmx6"]
        }

        self.assertEqual(type(pattern_dict), dict,
                         'Output of test_build_common_pattern_dict should be a dict')
        sorted_pattern_dict_test = {key: sorted(
            pattern_dict_test[key]) for key in sorted(pattern_dict_test)}

        sorted_pattern_dict = {key: sorted(
            pattern_dict[key]) for key in sorted(pattern_dict)}
        self.assertEqual(sorted_pattern_dict,
                         sorted_pattern_dict_test, 'dicts are not equal')

    def test_json_common_pattern_dict(self):
        try:
            from genestorian_module.summary_nltk_tags import json_common_pattern_dict
        except ImportError:
            raise Exception(
                'json_common_pattern_dict not imported from summary_nltk_tags')
        json_file = json_common_pattern_dict('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./common_pattern.json'),
                        'json_common_pattern_dict did not produce any json file')
        pattern_dict_test = {
            "GENE-MARKER": ["mug28::kanmx6"],
            "ALLELE": ["ura4-", "ade6-m216"],
            "GENE+-laci-TAG": ["his7+::laci-gfp"],
            "ALLELE-laco": ["lys1+::laco"],
            "GENE9-MARKER": ["mug29::kanmx6"]
        }
        sorted_pattern_dict_test = {key: sorted(
            pattern_dict_test[key]) for key in sorted(pattern_dict_test)}
        with open('common_pattern.json') as f:
            pattern_dict = json.load(f)
        sorted_pattern_dict = {key: sorted(
            pattern_dict[key]) for key in sorted(pattern_dict)}
        self.assertEqual(sorted_pattern_dict,
                         sorted_pattern_dict_test, 'dicts are not equal')

    def test_count_common_patterns(self):
        try:
            from genestorian_module.summary_nltk_tags import count_common_patterns
        except ImportError:
            raise Exception(
                'count_common_patterns not imported  from summary_nltk_tags')
        try:
            from genestorian_module.summary_nltk_tags import build_common_pattern_dict
        except ImportError:
            raise Exception(
                'build_common_pattern_dict not imported from summary_nltk_tags')
        txt_file = count_common_patterns('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./common_pattern_count.txt'),
                        'count_common_patterns did not produce any txt file')

        test_output = {
            "ALLELE": "2",
            "GENE-MARKER": "1",
            "GENE+-laci-TAG": "1",
            "ALLELE-laco": "1",
            "GENE9-MARKER": "1"
        }

        with open('common_pattern_count.txt', 'r') as f:
            output = {}
            for line in f:
                output[(line[:-3])] = line[-3:-1].strip()

        sorted_test_output = OrderedDict(sorted(test_output.items()))
        sorted_output = OrderedDict(sorted(test_output.items()))
        self.assertEqual(sorted_output, sorted_test_output,
                         'output file is not as expected')

    def test_count_most_common_other_tag(self):
        try:
            from genestorian_module.summary_nltk_tags import count_most_common_other_tag
        except ImportError:
            raise Exception(
                'count_most_common_other_tag not imported from summary_nltk_tags')
        tsv_file = count_most_common_other_tag('./alleles_pattern_nltk.json')
        self.assertTrue(os.path.isfile('./most_common_other_tag.txt'),
                        'count_common_patterns did not produce any most_common_other_tag.txt file')
        test_output = {
            "+":  "1",
            "laci": "1",
            "laco":  "1",
            "9":  "1"}
        with open('most_common_other_tag.txt', 'r') as f:
            output = {}
            for line in f:
                output[(line[:-3])] = line[-3:-1].strip()
        sorted_test_output = OrderedDict(sorted(test_output.items()))
        sorted_output = OrderedDict(sorted(output.items()))
        self.assertEqual(sorted_output, sorted_test_output,
                         'output not as expected')
