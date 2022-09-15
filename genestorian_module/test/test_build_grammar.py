from genericpath import isfile
import unittest


class TestBuildNltkTags(unittest.TestCase):
    def test_input_file_is_present(self):
        self.assertTrue(isfile('./nltk_trees_dataset/pseudo_grammar.json'),
                        'File pseudo_grammar.json not found')
