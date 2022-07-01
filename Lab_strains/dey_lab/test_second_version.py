import unittest
import os
import json


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
                         'feature_dict should return two values')
        self.assertEqual(len(output), 2,
                         'feature_dict should return two values')
        the_dict, the_name = output
        self.assertEqual(type(the_dict), dict,
                         'first return value should be a dictionary')
        self.assertEqual(the_name, 'MARKER',
                         'first return value should be MARKER')

    def test_strains_list(self):
        # This test imports build_strain_list from second_version_pipeline the function should be there
        # This function tests that you have renamed the function strains_list to build_strain_list
        # and that it does what it is specified in the issue

        try:
            from second_version_pipeline import strains_list
            raise Exception(
                'strains_list should have been renamed to build_strain_list')

        except ImportError:
            pass

        try:
            from second_version_pipeline import build_strain_list

        except ImportError:
            raise Exception(
                'strains_list should have been renamed to build_strain_list')

        strain_list = build_strain_list('strains_test.tsv')
        self.assertEqual(type(strain_list), list,
                         'Output of build_strain_list should be a list of dictionaries')

        self.assertEqual(type(strain_list[0]), dict,
                         'Output of build_strain_list should be a list of dictionaries')

        self.assertEqual(type(strain_list[1]), dict,
                         'Output of build_strain_list should be a list of dictionaries')

        strain_item_keys = list(strain_list[0].keys())

        strain_item_keys.sort()
        self.assertEqual(strain_item_keys, [
                         'alleles', 'genotype', 'id', 'mating_type'], 'The keys of the dictionary representing the strain should be \'alleles\', \'genotype\', \'id\', \'mating_type\'')

        self.assertEqual(strain_list[0]['id'], '1')
        self.assertEqual(strain_list[0]['genotype'],
                         'les1-mNeonGreen:Kan cut11-mCherry:ura4+ h+'.lower())
        self.assertEqual(strain_list[0]['mating_type'], 'h+')
        self.assertEqual(strain_list[0]['alleles'], [
                         'les1-mNeonGreen:Kan'.lower(), 'cut11-mCherry:ura4+'.lower()])

    def test_build_allele_feature_list(self):
        # This test imports build_allele_feature_list from second_version_pipeline the function should be there!
        # This function tests that you have renamed the function allele_feature_list to build_allele_feature_list
        # and that it does what it is specified in the issue

        try:
            from second_version_pipeline import allele_feature_list
            raise Exception(
                'allele_feature_list should have been renamed to build_allele_feature_list')

        except ImportError:
            pass

        try:
            from second_version_pipeline import build_allele_feature_list

        except ImportError:
            raise Exception(
                'allele_feature_list should have been renamed to build_allele_feature_list')

        example_input = ['cls1-36', 'ase1d:natmx']
        toml_files = [
            '../../data/alleles.toml',
            '../../data/gene_IDs.toml',
            '../../allele_components/tags.toml',
            '../../allele_components/markers.toml',
            '../../allele_components/promoters.toml'
        ]

        alleles_list = build_allele_feature_list(example_input, toml_files)

        self.assertEqual(type(alleles_list), list,
                         'Output of build_allele_feature_list should be a list of dictionaries')

        self.assertEqual(type(alleles_list[0]), dict,
                         'Output of build_allele_feature_list should be a list of dictionaries')

        self.assertEqual(type(alleles_list[1]), dict,
                         'Output of build_allele_feature_list should be a list of dictionaries')

        allele_item_keys = list(alleles_list[0].keys())

        allele_item_keys.sort()

        self.assertEqual(allele_item_keys, [
                         'allele_features', 'name', 'pattern'], 'The keys of the dictionary representing the allele should be \'allele_features\', \'name\', \'pattern\'')

        with open('alleles_test.json') as ins:
            expected_output = json.load(ins)

        self.assertEqual(alleles_list, expected_output)
