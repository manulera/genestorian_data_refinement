# Genestorian data refinement

A project to extract genotype information from lab spreadsheets.

## Quickstart ⏲️

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Download some necessary data to find fluorescence protein
python get_fpbase_data.py ../allele_components/tags_fpbase.toml

# Start a dev server
uvicorn api:app --reload
```

Go to http://127.0.0.1:8000, and you should be able to try the example.

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
### Working with Docker

To build from the dockerfile available in the repo:
```
docker build -t genestorian_data_refinement .
docker run -d --name genestorian_data_refinement_container -p 8000:80 genestorian_data_refinement

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
`markers.toml`, `promoters.toml`, `tags.toml`, `sequence_features.toml` contains common markers, promoters, tags and sequence  features used in S Pombe labs. The format of the toml file is:

```toml
[feature_type.<name of the feature>]
name = '<name of the feature>'
reference = ''
synonyms = []

# For example
[gene."SPAC1002.06c"]
ref = "SPAC1002.06c"
name = "bqt2"
synonyms = [ "mug18", "rec23",]

[tag.avGFP]
name = "avGFP"
reference = "10.1016/0378-1119(92)90691-h"
synonyms = [ "wtGFP", "GFP", "gfp10", "Green Fluorescent Protein",]

```

### Retrieving fluorescent protein tags from FPBase

You can generate the file `allele_components/tags_fpbase.toml`, which contains many of the known fluorescent protein tags in the above format from fp_base(https://www.fpbase.org/). To do this go to the folder `get_data` and run:

```bash
python get_fpbase_data.py ../allele_components/tags_fpbase.toml
```

This script retrieves the data from fb_base graphql API(https://www.fpbase.org/graphql/).

## Running the Pipeline

The goal of this pipeline is to extract the alleles from genotype, identify the patterns followed by the alleles and structure the data in a way that it could be migrated to a database.
At present, the pipeline extracts alleles from the genotype to a list. It identifies different features of alleles to  tokenize and tag the features.The tagged tokens are then parsed by NLTK RegexParser using the rules defined by us. The output of the parser is a tree with identified patterns as subtrees. The input of the pipeline must be a tsv file, typically named `strains.tsv` with column names 'strain_id' and 'genotype' which contain strain id and genotype of a strain. 

```tsv
strain_id	 genotype
FY14021	 h+ leu1-32 ura4-D18 ade6-M210 dlp1::ura4	
FY14075	 h- ade6-M210 cdc25-22
```

### Formatting the input data

Because strain lists from different labs have different formats, you have to convert them to the format above. You can find scripts named `format.py` that takes the excel file as input and generates `strains.tsv` for each of the strain lists in the `Lab_strains` folder. `format.py` essentially, reads the strain id column and genotype column to `strains.tsv` file.

To generate a valid `strains.tsv` for your strain list, write your own `format.py`. For example, for the public strain list `Lab_strains/nbrp_strains`, extracts id and genotype from 'NBRPID' and 'genotype' column. It also calls na_filter=False to identy the empty rows and avoid reading them as NAN.

```
import pandas as pd

read_file = pd.read_csv('strains_raw.tsv', usecols=[
                        'NBRPID', 'genotype'], na_filter=False, sep='\t')
read_file = read_file.rename(
    columns={'NBRPID': 'strain_id'})
read_file.to_csv('strains.tsv', sep='\t', index=False)
```

### Build nltk tags

We are using nltk library to process tha data. Before using the nltk library, it's important to have data structured in a format which can be input to nltk parser.

The script `build_nltk_tags` in `genestorian_module` takes `strains.tsv` as an input and creates a file named `alleles_pattern_nltk.json` in the same directory of `strains.tsv`. To run this script:

```
python /path/to/genstorian_module/build_nltk_tags.py /path/to/strains.tsv
```

For each allele in the input file `strains.tsv`, it identifies the allele features such as allele, gene, tag , marker etc and extracts them in a list along with a tag, then outputs a list of dict, where each entry represents an allele. Each dict in the list has two fields:

* `name`: allele_name
* `pattern`: this is the list of features extracted along with the tags extracted from allele_name
  
From this example tsv

```tsv
Column 1	Column 2
FY21859	h90 mug28::kanMX6 ade6-M216 ura4- his7+::lacI-GFP lys1+::lacO
FY21860	h90 mug29::kanMX6 ade6-M216 ura4- his7+::lacI-GFP lys1+::lacO
```

The output is:

```
[
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
```

You can run this for the example strain list `Lab_strains/nbrp_strains/strains.tsv` by running:

```
 python build_nltk_tags.py ../../Lab_strains/nbrp_strains/strains.tsv
```

### Find common patterns

The script `summary_nltk_tags.py` in `genestorian_module` takes `alleles_pattern_nltk.json` as input and creates 3 files with file names 'common_pattern.json' , 'common_pattern_count.txt' and 'most_common_other_tag.txt' in the same directory that of `alleles_pattern_nltk.json`
To run this script:
```
python /path/to/genstorian_module/summary_nltk_tags.py /path/to/alleles_pattern_nltk.json
```
It finds the common pattern followed by alleles and makes a dictionary where the key is the pattern and the value is the list of occurrence of that pattern. This dict is written into the json file `common_pattern.json`. Then, it counts the number of times the same pattern occurs and outputs it in the text file `common_pattern_count.txt` in decreasing order of occurrence. The script also counts the most common features with are not identified by our pipeline and it is written in another text file `most_common_other_tag.txt`, again in decreasing order of occurence. 


You can run this for the example strain list `Lab_strains/nbrp_strains/alleles_pattern_nltk.json` by running:

```
 python summary_nltk_tags.py ../../Lab_strains/nbrp_strains/alleles_pattern_nltk.json 

 ```
For the above example in Build nltk tags, the output would look like:

 `common_pattern.json`
```
{
   "GENE-MARKER" : ["mug28::kanmx6"],
   "ALLELE" : ["ade6-m216", "ura4-"],
   "GENE+-laci-TAG" : ["his7+::laci-gfp"],
   "ALLELE-laco": ["lys1+::laco"],
   "GENE9-MARKER": ["mug29::kanmx6"]
}
```
`common_pattern_count.txt` 

```
ALLELE 2
GENE-MARKER 1 
GENE+-laci-TAG 1 
ALLELE-laco 1
GENE9-MARKER 1
```

`most_common_other_tag.txt`

```
+ 1
laci 1
laco 1
9 1

```

### Grammar for NLTK Regex Chunk Parser

We use NLTK Regex chunk Parser to parse the allele names. The grammar is the set of chunk rules defined to parse the allele names. Because the data that we work with is much more complicated compared to the text usually parsed using nltk. Hence we have defined a pseudo grammar which is first, used to build the chunk rules and later in the process, it is used to further parse the chunked patterns.

To build your own grammar: you need a json file which contains a dictionary where the keys are the rule name and value of the key is an other dictionary. In the other dictionary keys are pattern and other regex demonstrated in the example below. other_regex is the regex which should match to the value of other tag in the pattern to correctly identify the pattern.

```
{
   "GENE_DELETION": {
      "pattern": "<GENE><->?<other>?<->?<MARKER>",
      "other_regex": [
         "^(delta|δ|del)$"
      ]
   },
   
   "PROMOTER_GENE": {
      "pattern": "<other><GENE><-><GENE>",
      "other_regex": [
         "(?<![a-z])p$"
      ]
   },

   "C_Terminal_Tagging": {
      "pattern": "<GENE><->?<TAG><->?<MARKER>",
      "other_regex": []
   }
}
```

Save this dict, e.g. in `grammar/pseudo_grammar.json`.

Then, call `python genestorian_module/genestorian_module/build_grammar.py grammar/pseudo_grammar.json grammar/grammar.txt` on that file, and specify an output text file (in this case `grammar/grammar.txt`).

This creates a `grammar.txt` file in `genestorian_module/genestorian_module/grammar` directory. Text file from above example would look like:

```
      GENE_DELETION {<GENE><->?<other>?<->?<MARKER>}
      PROMOTER_GENE : {<other><GENE><-><GENE>}
      C_Terminal_Tagging : {<GENE><->?<TAG><->?<MARKER>}
```

### Identify patterns using NLTK RegexChunker
We use NLTK Regex Chunker along with the regex defined in pseudo_grammar to identify patterns in allele names. The RegexChunk Parser first identifies the patterns in the `grammar.txt` then builds a tree. Then the other_regex in pseudo_grammar is matched to the value of the 'other' token in the subtree(the identified pattern tree in the tree) to validate the tree. If the value of other tag is matched then only the pattern identified by the chunker is labelled otherwise the identified pattern tree is discarded. In some cases, only a part of the 'other' token value is matched, in such cases the value is split and only the matched part is added to the tree, remaining part is added to outside the identified pattern tree.

To identify patterns in your alleles run `python build_nltk_trees.py  /path/to/alleles_pattern_nltk.json`
in `genestorian_module/genestorian_module/`. This creates a file `nltk_trees.json` in the same dictory as that of `alleles_pattern_nltk.json`. The file contains a dictionary in which keys are the allele names and value is the tree 

for example alleles: 
```
pht1kanmx6
ade6-m210<<ade6+:mfm1-y31i
leu1-32:pnpg1-npg1-gfp-tadh1-ura4+

```
The output for above example looks like:

```
{
   "pht1kanmx6" : "(S (GENE_DELETION (GENE pht1) (MARKER kanmx6)))",
   "ade6-m210<<ade6+:mfm1-y31i": "(S (ALLELE ade6-m210) (- <<) (GENE ade6) (other +) (- :) (ALLELE_AA_SUBSTITUTION (GENE mfm1) (- -) (other y31i)))",
   "leu1-32:pnpg1-npg1-gfp-tadh1-ura4+": "(S (ALLELE leu1-32) (- :) (PROMOTER_GENE (other p) (GENE npg1) (- -) (GENE npg1)) (- -) (TAG gfp) (- -) (other t) (GENE adh1) (- -) (ALLELE ura4+))",
}
```

## End-to-End Pipeline

WIP