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

## Running the Pipeline

### Read the excel file

Each lab has a `format.py` to pre-process the data before converting into a tsv file. It should extracts the strain_id and genotype from the input file and save in `strains.tsv` file

1. `strains.tsv` file has genotype and strain_id column.
2. Import the function `excel_to_tsv(excel_file, read_cols, tsv_file)` from `genestorian_module` to convert the excel file to tsv. The arguments passed to the function are path of excel file, columns to be read i.e [column to be used as strain id, genotype] and 'strains.tsv'
3. Some excel file require pre-processing before converting them to tsv. Excel file should have strain_id and genotype as column name. Add strain_id column to excel file if not present already.
4. Your data might not be in an excel file. In such cases, read the genotype and strain_id column from the input file and write into a tsv file. 
Eg: `Lab_strains/nbrp_strains/format.py` reads 'NBRPID'and 'genotype' column from raw_strains.csv. It renames the 'NBRPID' to 'strain_id'. Then, it writes into a tsv file.
NOTE: When you are not using `excel_to_tsv` to read to csv, make sure to deal with the special characters present in your data.

### Build nltk tags
We are using nltk library to process tha data. Before using the nltk library, it's important to have data structured in a format which can be input to nltk APIs. 
`build_nltk_tags` takes strains.tsv as input. It makes a list of allele names from the genotype. Then, it identifies features in the allele name and add a tag to features. Features which aren't catergorised as gene, allele, marker or tag are tagged as 'other'. The output is a dict saved in a json file. The output dict has allele name and allele pattern.

To build your own nltk tags for strains, in `genestorian_module/genestorian_module/` directory run `python build_nltk_tags ../../Lab_strains/lab_name/strains.tsv`. This generates nltk tags and patterns in respective lab directory.
Eg:
NBRP strains in `Lab_strains` directory has `strains.tsv` file which has two columns strain_id and genotype. 
In `genestorian_module/genestorian_module/` directory run `python build_nltk_tags ../../Lab_strains/nbrp_strains/strains.tsv`. 
This generates alleles_nltk.json in `Lab_strains/nbrp_strains/`. 

### Summarize nltk tags
1. To find the alleles that follow same patterns:
Import `json_common_pattern_dict` from `genestorian_module`. `json_common_pattern_dict` takes argument alleles_ntlk.json. This generates a file 'common_pattern.json' file in the respective lab directory. 
2. To count the most commonly occurring features which are tagged with 'other' tag:
Import `count_most_common_other_tag` from `genestorian_module`. `count_most_common_other_tag` takes argument alleles_nltk.json. This generates a file 'most_common_other_tag.tsv' file in the respective lab directory. 
 





