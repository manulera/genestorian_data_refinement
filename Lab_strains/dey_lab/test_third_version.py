import unittest
import os
import json


class TestThirdVersion(unittest.TestCase):
    def test_that_file_is_present(self):
        self.assertTrue(os.path.isfile('./alleles.json'),
                        'The file alleles.json could not be found')

        try:
            from second_version_pipeline import build_strain_list
        except ImportError:
            raise Exception(
                'build_strain_list not imported from second_version_pipeline')
        try:
            from second_version_pipeline import build_allele_feature_list
        except ImportError:
            raise Exception(
                'build_allele_feature_list not imported from second_version_pipeline')

        toml_files = [
            '../../data/alleles.toml',
            '../../data/gene_IDs.toml',
            '../../allele_components/tags.toml',
            '../../allele_components/markers.toml',
            '../../allele_components/promoters.toml'
        ]
        strain_list = build_strain_list('strains.tsv')
        allele_names = set({})
        for strain in strain_list:
            allele_names.update(strain['alleles'])

        allele_feature_list = build_allele_feature_list(
            allele_names, toml_files)

        for allele in allele_feature_list:
            for allele_feature in allele['allele_features']:
                for coords in allele_feature['coords']:
                    start_coord = coords[0]
                    end_coord = coords[1]
                    self.assertTrue(
                        allele['name'][start_coord:end_coord+1], allele_feature['name'], ' not equal')
