import unittest
import os
import re


class TestBuildNltkTags(unittest.TestCase):
    def test_all_input_files_are_present(self):
        parent_dir = '../../Lab_strains'
        path_list_strain_file = []
        # path_list_allele_json_file = []
        for dir in os.listdir(parent_dir):
            path = os.path.join(parent_dir, dir)
            files_strain = os.path.join(path + '/strains.tsv')
            path_list_strain_file.append(files_strain)
        for strain_file_path in path_list_strain_file:
            self.assertTrue(os.path.isfile(strain_file_path),
                            'The file strains.tsv not found')

    def test_build_nltk_tag(self):
        try:
            from genestorian_module.build_nltk_tags import build_nltk_tag
        except ImportError:
            raise Exception(
                'build_nltk_tag not imported from fourth_version_pipeline')
        try:
            from genestorian_module.third_version_pipeline import build_strain_list
        except ImportError:
            raise Exception(
                'build_strain_list not imported from third_version_pipeline')

        strain_list = build_strain_list('./test_strains.tsv')
        allele_names = set({})
        for strain in strain_list:
            allele_names.update(strain['alleles'])
        toml_files = [
            '../../data/alleles.toml',
            '../../data/gene_IDs.toml',
            '../../allele_components/tags.toml',
            '../../allele_components/tags_fpbase.toml',
            '../../allele_components/markers.toml',
            '../../allele_components/promoters.toml'
        ]
        alleles_list = build_nltk_tag(allele_names, toml_files)
        for allele in alleles_list:
            allele_name = ''
            feature_start_coords = []
            for feature in allele["pattern"]:
                allele_name += feature[0]
            self.assertEqual(
                allele['name'], allele_name, ' pattern list does not add up to allele name')

            coords = [i.start() for i in re.finditer(
                re.escape(feature[0]), allele['name'])]
            feature_start_coords.append(coords[0])
            self.assertEqual(feature_start_coords,
                             sorted(feature_start_coords), 'allele features are not sorted according to the appearance in allele name')
            name = allele["name"]
            pattern_names_joined = ''
            for pattern_name in allele["pattern"]:
                pattern_names_joined += pattern_name[0]
            self.assertEqual(name, pattern_names_joined,
                             'allele name does not match the name formed by joining the pattern names')

    def test_main_function(self):
        try:
            from genestorian_module.build_nltk_tags import main
        except ImportError:
            raise Exception(
                'main not imported from fourth_version_pipeline')

        input_file = './test_strains.tsv'
        output_file = main(input_file)
        self.assertTrue(os.path.isfile('./alleles_pattern_nltk.json'),
                        'The alleles_nltk.json not found')
