# Genestorian data refinement

A project to extract genotype information from lab spreadsheets.

## Installing

For the python dependencies management, we will use [poetry](https://python-poetry.org/). To install the dependencies use:

```
poetry install
```

If this is the first time you install the dependencies for the project, this will create a new virtual environment inside a folder .venv in the project folder (see `poetry.toml` where it's configured that the virtual environment will be created in the containing folder). This is convenient to set the vscode settings (in the folder `.vscode`).

From now on, if you want to use this environment you can either:

* Call python by doing `poetry run python ...` everytime you run something.
* Activate the environment by running `python shell`.

### Adding new dependencies

To add new dependencies, run `poetry install library_name`.

### Working with notebooks and ipython scripts

You can add the virtual environment that you created to the jupyter kernel by running:

```
poetry run python -m ipykernel install --user
```

## Getting the data

### Strain lists

For now, we start with the publicly available strain list that can be found in https://yeast.nig.ac.jp/yeast/fy/StrainAllItemsList.xhtml

To get the data in there as tsv files, we scrape the website using the js script in the `get_data` folder, which returns a bunch of `tsv` files that are combined in the file `data/strains.tsv`. The important columns:

* PMID: the pubmed IDs of the publications where the strains were used. Many of the rows are empty, some have more than one id concatenated one after the other (a PMID has 8 numbers and you can use to access a publication in pubmed. For example, for 35293864, the url is https://pubmed.ncbi.nlm.nih.gov/35293864/)
* NBRPID: The unique ID of the strain within this strain bank.
* strain_name: the ID/name of the strain in the submitter lab collection.
* genotype: the genotype of the strain -> What we care about!
* source: the lab head who submitted the strain. This can be useful because probably each lab has a different 'style' when naming their strains.

The rest we can ignore for now.

### Gene names and synonyms

File `data/gene_IDs_names.tsv` we get from Pombase: https://www.pombase.org/data/names_and_identifiers/gene_IDs_names.tsv

It has three columns:

1. Systematic pombase ID
2. Main gene name (this may be empty)
3. Gene synonyms, comma separated (it may be empty, but it may also be filled when the previous field is empty 😮)

### Gene and alleles

File `data/alleles_pombemine.tsv` contains all the alleles we can find in pombase. This can be accessed from pombemine (http://pombemine.rahtiapp.fi/pombemine/querybuilder), with the xml query in `get_data/pombemine_query.xml`.

It has 5 columns:

1. Systematic ID in pombase (will match first column in `data/gene_IDs_names.tsv`)
2. Main gene name in pombase (will match second column in `data/gene_IDs_names.tsv`)
3. Allele name (if we are lucky we find it in the `genotype` column in `data/strains.tsv`)
4. Description (some info about the allele sequence). For now we won't use it.
5. Expression (expression level in the experiment. In general reflects a change in the promoter.). For now we won't use it.
 
### Other features
The folder `alleles_components` contains a bunch of toml files. Each toml file corresponds to one feature type.
`markers.toml`, `promoters.toml`, `tags.tom`, `sequence_features.tom` contains common markers, promoters, tags and sequence  features used in S Pombe labs. The format of the toml file is as:
```
[feature_name.<name of the feature>]
name = '<name of the feature>'
reference = ''
synonyms = [synonyms]
```

* `tags_fpbase.toml` contains fluorescent protein tags from fp_base(https://www.fpbase.org/), which can be accessed from fb_base graphql API(https://www.fpbase.org/graphql/), with graphql in `get_data/get_fpbase_data.py`

  

## Running the Pipeline

The input for the pipeline is the excel sheet which contains a unique stain id, genotype and other strain related information. The strain_id and the genotype are only two columns used by the pipeline.

### Read the excel file
Each lab has a `format.py` to pre-process the data before converting into a tsv file. It should extracts the strain_id and genotype from the input file and save in `strains.tsv` file

##### To generate your own `strains.tsv`:
* Import the function `excel_to_tsv(excel_file, read_cols, tsv_file)` from `genestorian_module` to convert the excel file to tsv. The arguments passed to the function are path of excel file, columns to be read i.e [column to be used as strain id, genotype] and 'strains.tsv'
* Some excel file require pre-processing before converting them to tsv. 
* Your data might not be in an excel file. In such cases, read the genotype and strain_id column from the input file and write into a tsv file. 
Eg: 
```
import pandas as pd

read_file = pd.read_csv('strains_raw.tsv', usecols=[
                        'NBRPID', 'genotype'], na_filter=False, sep='\t')
read_file = read_file.rename(
    columns={'NBRPID': 'strain_id'})
read_file.to_csv('strains.tsv', sep='\t', index=False)
```
NOTE: When you are not using `excel_to_tsv` to read the input file, make sure to deal with the special characters present in your data.

### Build nltk tags
We are using nltk library to process tha data. Before using the nltk library, it's important to have data structured in a format which can be input to nltk APIs. 
`build_nltk_tags` in the genestroian_module adds feature tags to the allele extracted from the genotype in strains.tsv.
`build_nltk_tags` takes strains.tsv as input. The output looks somethings like:
```[{
      "name": "e152k)-mcherry:kanr",
      "pattern": [ [ "e152k)", "other" ], [ "-", "-" ], [ "mcherry", "TAG" ], [ ":", "-" ], [ "kanr", "MARKER" ] ]
   },
   {
      "name": "cdc13-m7<<hygr",
      "pattern": [ [ "cdc13-m7", "ALLELE" ], [ "<<", "-" ], [ "hygr", "MARKER" ] ]
   }]
```
This output is saved by default in the `allele_pattern_nltk.json` in the same directory that of `strains.tsv`.

#### To build your own nltk tags for strains
* In `genestorian_module/genestorian_module/` directory run `python build_nltk_tags ../../Lab_strains/lab_name/strains.tsv`. 
Eg:
NBRP strains in `Lab_strains` directory has `strains.tsv` file which has two columns strain_id and genotype. 

In `genestorian_module/genestorian_module/` directory run `python build_nltk_tags ../../Lab_strains/nbrp_strains/strains.tsv`. 
This generates a file `allele_pattern_nltk.json` in `Lab_strains/nbrp_strains/`. 
#### How build_nltk_tags works
* It starts with a list of genotype from the strains.tsv which is essentially the input.
* From the list of the genotype, a list of alleles is extracted. 
* A feature dict is built for each toml file present in allele_components directory(others.toml not being used at present). The keys in the feature dict are name and synonyms of the features in the feature toml file.
* Whenever any part of allele is matched to the key  of the feature dict, it is added to the pattern, along with the tag.
* Separators are identified in the allele name and tagged as '-'.
* Parts of allele name which aren't identfied as an allele feature or separator are tagged as 'other'
  

### Summarize nltk tags
You can have a look at alleles which follow similar patterns, count the number of alleles following same pattern and look at the most frequently occurring features tagged with other's tag.
##### To find the alleles that follow same patterns:
Import `json_common_pattern_dict` from `genestorian_module`. `json_common_pattern_dict` takes argument alleles_ntlk.json. This generates a file 'common_pattern.json' file in the respective lab directory. 
##### To count the number of alleles that follow same pattern:
Import `count_most_common_other_tag` from `genestorian_module`. `count_common_patterns` takes argument alleles_nltk.json. This generates a file 'most_common_other_tag.tsv' file in the respective lab directory.
##### To count the most commonly occurring features which are tagged with 'other' tag:
Import `count_most_common_other_tag` from `genestorian_module`. `count_most_common_other_tag` takes argument alleles_nltk.json. This generates a file 'most_common_other_tag.tsv' file in the respective lab directory. 
eg:
```

from genestorian_module.summary_nltk_tags import (json_common_pattern_dict,
                                                  count_common_patterns,
                                                  count_most_common_other_tag)

json_common_pattern_dict('alleles_nltk.json')
count_common_patterns('alleles_nltk.json')
count_most_common_other_tag('alleles_nltk.json')
```





