import unittest
import os
import re
import json


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
            for feature in allele["pattern"]:
                allele_name += feature[1][0]
            self.assertEqual(
                allele['name'], allele_name, ' pattern list does not add up to allele name')

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
        test_output = [
            {
                "name": "his7+::laci-gfp",
                "pattern": [["GENE", ["his7"]], ["other", ["+"]], ["-", ["::"]], ["other", ["laci"]], ["-", ["-"]], ["TAG", ["gfp"]]]
            },
            {
                "name": "ura4-",
                "pattern": [["ALLELE", ["ura4-"]]]
            },
            {
                "name": "lys1+::laco",
                "pattern": [["ALLELE", ["lys1+"]], ["-", ["::"]], ["other", ["laco"]]]
            },
            {
                "name": "mug28::kanmx6",
                "pattern": [["GENE", ["mug28"]], ["-", ["::"]], ["MARKER", ["kanmx6"]]]
            },
            {
                "name": "ade6-m216",
                "pattern": [["ALLELE", ["ade6-m216"]]]
            },
            {
                "name": "mug29::kanmx6",
                "pattern": [["GENE", ["mug2"]], ["other", ["9"]], ["-", ["::"]], ["MARKER", ["kanmx6"]]]
            }
        ]
        with open('alleles_pattern_nltk.json') as f:
            output = json.load(f)
        sorted_test_output = sorted(test_output, key=lambda d: d['name'])
        sorted_output = sorted(output, key=lambda d: d['name'])
        self.assertEqual(sorted_output, sorted_test_output,
                         'output of main() is not as expected ')
