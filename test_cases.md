
class TestSecondVersionPipeline(unittest.TestCase):
    test_that_test_files_are_there(self):
        self.assertTrue(os.path.isfile('./strains_test.tsv'))tests whether strains_test.tsv file is present or not

    test_read_strains_tsv(self):
    try:
            from genestorian_module import read_strains_tsv
        except ImportError:
            raise Exception(
                'You have to create the function read_strains_tsv in `genestorian_module/genestorian_module/__init__.py`')
        imports read_strains_tsv from genestorian_module/genestorian_module/__init__.py
        if read_strain_tsv not found then it raises an error genestorian_module/genestorian_module/__init__.py`and the test fails


    self.assertEqual(type(row['Genotype']), str,
                             'read_strains_tsv should convert genotypes to strings') tests if type of row(['Genotype']) is str

    self.assertEqual(row['Genotype'], row['Genotype'].lower(),
                             'read_strains_tsv should make genotypes lowercase') tests if row['Genotype'] is lowercase
    
    def test_feature_dict(self):
    self.assertEqual(type(output), tuple,
                         'feature_dict should return two arguments') checks if type of output is tuple or not. Fails if output isn't tuple

    self.assertEqual(len(output), 2,
                         'feature_dict should return two arguments') fails if len of output isn't 2

    self.assertEqual(type(the_dict), dict,
                         'first return value should be a dictionary') checks the type of first value of return from build_feature_dict()
    self.assertEqual(the_name, 'MARKER',
                         'first return value should be MARKER')
                         checks the value of 2nd return from build_feature_dict()
