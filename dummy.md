For the function `allele_feature_list`:

A function name should always contain a verb, `allele_feature_list` sounds like a variable name.

* [ ] Replace all function names that don't have verbs in them (in all files).

A few suggestions to improve the code.

* [ ] The `replace_word` parameter that you pass to functions `replaced_allele_feature_name` and `replaced_allele_feature` is not necessary, it can be extracted from the dictionary, and made uppercase. You can make the function `feature_dict` return `feature_type_name` as well, and then make it uppercase.

Your function `replaced_allele_feature_name` takes a list as an argument. However, you are iterating over the alleles and passing each allele in a list again:

https://github.com/manulera/genestorian_data_refinement/blob/704b546494d662bb79c6600eebc5cff8bc2be842/Lab_strains/dey_lab/second_version_pipeline.py#L61

https://github.com/manulera/genestorian_data_refinement/blob/704b546494d662bb79c6600eebc5cff8bc2be842/Lab_strains/dey_lab/second_version_pipeline.py#L65

This can be confusing for the person reading the code, and also it's not efficient because you are reading all the toml files for each allele again. You can see that it takes extremely long!

* [ ] Improve `replaced_allele_feature_name` as indicated below

Once you have addressed the point above mentioning `replace_world`, you can then write a function that takes two arguments:

* The `allele_names` list as before, and do something in these lines:

```python

def allele_feature_list(allele_names, toml_files):

    # Create an empty dictionary in the desired format:
    output_list = list()
    for allele_name in allele_names:
        output_list.append{
            'name': allele_name,
            'pattern': allele_name, # This is where you will substitute
            'allele_features': []
        }

    # Do a replacement for each toml file.
    for toml_file in toml_files:

        synonyms_2toml_key_dict = get_feature_dict(toml_file)

        for allele_dict in output_list:
            
        # This function should edit the values directly in the dictionary, so no need to return an output
        replaced_allele_feature_name(toml_file, output_list)
    
    return output_list

```


