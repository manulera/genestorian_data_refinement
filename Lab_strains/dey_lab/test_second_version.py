import unittest
import os


class TestSecondVersionPipeline(unittest.TestCase):

    def test_that_test_files_are_there(self):
        self.assertTrue(os.path.isfile('./strains_test.tsv'),
                        'The file strains_test.tsv could not be found')

    def test_read_strains_tsv(self):
        # This function tests that you have created a function read_strains_tsv
        # in `genestorian_module/genestorian_module/__init__.py` and that it performs the tasks
        # described in the issue
        try:
            from genestorian_module import read_strains_tsv
        except ImportError:
            raise Exception(
                'You have to create the function read_strains_tsv in `genestorian_module/genestorian_module/__init__.py`')
        data = read_strains_tsv('strains.tsv')

        for row_index, row in data.iterrows():
            self.assertEqual(type(row['Genotype']), str,
                             'read_strains_tsv should convert genotypes to strings')
            self.assertEqual(type(row['Sample Name']), str,
                             'read_strains_tsv should convert Sample Name to strings')
            self.assertEqual(row['Genotype'], row['Genotype'].lower(),
                             'read_strains_tsv should make genotypes lowercase')

    def test_feature_dict(self):
        # This function tests that you have renamed the function feature_dict to build_feature_dict
        # and that it does what it is specified in the issue

        try:
            from genestorian_module.replace_feature import feature_dict
            raise Exception(
                'feature_dict should have been renamed to build_feature_dict')

        except ImportError:
            pass

        try:
            from genestorian_module.replace_feature import build_feature_dict

        except ImportError:
            raise Exception(
                'feature_dict should have been renamed to build_feature_dict')

        output = build_feature_dict('../../allele_components/markers.toml')

        self.assertEqual(type(output), tuple,
                         'feature_dict should return two arguments')
        self.assertEqual(len(output), 2,
                         'feature_dict should return two arguments')
        the_dict, the_name = output
        self.assertEqual(type(the_dict), dict,
                         'first return value should be a dictionary')
        self.assertEqual(the_name, 'MARKER',
                         'first return value should be MARKER')

    def test_feature_dict(self):
        # This functions tests
        pass
