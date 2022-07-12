

```python
class TestSecondVersionPipeline(unittest.TestCase):
test_that_test_files_are_there(self):
    self.assertTrue(os.path.isfile('./strains_test.tsv'))
```
checks if strains_test.tsv file is present. If found then pass else fails

```
test_read_strains_tsv(self):
            try:
                from genestorian_module import read_strains_tsv

            except ImportError:
                raise Exception(
                    'You have to create the function read_strains_tsv in `genestorian_module/genestorian_module/__init__.py`') 
```
imports read_strains_tsv from genestorian_module/genestorian_module/__init__.py .  If read_strain_tsv not found then it gives an error genestorian_module/genestorian_module/__init__.py`and the test fails due to Import error
```
            self.assertEqual(type(row['Genotype']), str,
                        'read_strains_tsv should convert genotypes to strings') 
```
Checks if type of row(['Genotype']) is str. If not then test fails with error 'read_strains_tsv should convert genotypes to strings'

```
self.assertEqual(row['Genotype'], row['Genotype'].lower(),
                             'read_strains_tsv should make genotypes lowercase') 
```
Checks if row['Genotype'] is lowercase. If not then the test fails with error 'read_strains_tsv should make genotypes lowercase'

```
def test_feature_dict(self):
    self.assertEqual(type(output), tuple,
                'feature_dict should return two arguments') 
```
checks if type(output) == tuple. Fails if output isn't tuple

```
self.assertEqual(len(output), 2,
            'feature_dict should return two arguments') 
```

checks if len(outfput) == 2. If not then fails with error 'feature_dict should return two arguments'
```
self.assertEqual(type(the_dict), dict,
            'first return value should be a dictionary') 
```
checks the type of first value of return from build_feature_dict()
if type(the_dict) == dict , then pass else fails with error 'first return value should be a dictionary'

```
self.assertEqual(the_name, 'MARKER',
            'first return value should be MARKER')
```
checks the value of 2nd return from build_feature_dict()
checks if the_name == 'MARKER' 

```
def test_strains_list(self):
    try:
        from second_version_pipeline import strains_list
    raise Exception(
        'strains_list should have been renamed to build_strain_list')
        
    except ImportError:
        pass
```
Imports strain list from second_version_pipeline, if found the then throws exception error 'strains_list should have been renamed to build_strain_list'). The exception is then passed.

    try:
        from second_version_pipeline import build_strain_list

    except ImportError:
        raise Exception(
        'strains_list should have been renamed to build_strain_list')
Imports strain list from second_version_pipeline, if not found the then throws exception error 'strains_list should have been renamed to build_strain_list'). 

    strain_list = build_strain_list('strains_test.tsv')
    self.assertEqual(type(strain_list), list,
                'Output of build_strain_list should be a list of dictionaries')
checks type(strain_list) ==list. If not then gives an error 

    self.assertEqual(type(strain_list[0]), dict,
                'Output of build_strain_list should be a list of dictionaries')

    self.assertEqual(type(strain_list[1]), dict,
                'Output of build_strain_list should be a list of dictionaries')

    strain_item_keys = list(strain_list[0].keys())

    strain_item_keys.sort()
    self.assertEqual(strain_item_keys, [
                'alleles', 'genotype', 'id', 'mating_type'], 'The keys of the dictionary representing the strain should be \'alleles\', \'genotype\', \'id\', \'mating_type\'')

    self.assertEqual(strain_list[0]['id'], 1)
    self.assertEqual(strain_list[0]['genotype'],
                'les1-mNeonGreen:Kan cut11-mCherry:ura4+ h+'.lower())
    self.assertEqual(strain_list[0]['mating_type'], 'h+')
    self.assertEqual(strain_list[0]['alleles'], [
                'les1-mNeonGreen:Kan'.lower(), 'cut11-mCherry:ura4+'.lower()])

--

    def test_build_allele_feature_list(self):

        try:
            from second_version_pipeline import allele_feature_list
        raise Exception(
            'allele_feature_list should have been renamed to build_allele_feature_list')

imports allele_feature_list from second version pipeline, if not found then throws an exception

    except ImportError:
        pass

    try:
        from second_version_pipeline import build_allele_feature_list

    except ImportError:
        raise Exception(
            'allele_feature_list should have been renamed to build_allele_feature_list')

imports build_allele_feature_list from second version pipeline, if not found then throws above exception

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

Checks if the type(alleles_list) == list, if not then throws error 'Output of build_allele_feature_list should be a list of dictionaries'


    self.assertEqual(type(alleles_list[0]), dict,
                'Output of build_allele_feature_list should be a list of dictionaries')

Checks if the type(alleles_list[0]) == dict, if not then throws error 'Output of build_allele_feature_list should be a list of dictionaries'


    self.assertEqual(type(alleles_list[1]), dict,
                'Output of build_allele_feature_list should be a list of dictionaries')
similar to previous assert 

    allele_item_keys = list(alleles_list[0].keys())

    allele_item_keys.sort()

    self.assertEqual(allele_item_keys, [
                'allele_features', 'name', 'pattern'], 'The keys of the dictionary representing the allele should be \'allele_features\', \'name\', \'pattern\'')
Checks if allele_item keys == ['allele_features', 'name', 'pattern'] if not then gives error 'The keys of the dictionary representing the allele should be 'allele_features', 'name', 'pattern''.

    with open('alleles_test.json') as ins:
        expected_output = json.load(ins)

    self.assertEqual(alleles_list, expected_output)

checks if allele list is equal to the expected output in the alleles_test.json file
