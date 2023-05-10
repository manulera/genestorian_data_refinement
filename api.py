from fastapi import FastAPI, Query
from starlette.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from genestorian_module.build_nltk_tags import build_nltk_tag
from genestorian_module.build_nltk_trees import apply_pseudo_grammar, post_process_pseudo_grammar
import json
from nltk.tree import ParentedTree, TreePrettyPrinter


def name2pattern(allele_name):

    toml_files = [
        'data/alleles.toml',
        'data/gene_IDs.toml',
        'allele_components/tags.toml',
        'allele_components/tags_fpbase.toml',
        'allele_components/markers.toml',
        'allele_components/promoters.toml',
        'allele_components/sequence_features.toml'
    ]

    alleles_list = build_nltk_tag([allele_name.lower()], toml_files, "allele_components/separators.txt")
    return alleles_list[0]['pattern']


# The class for the response
class ProcessAlleleResponse(BaseModel):
    name: str
    pattern: list[tuple[str, list[str]]]


app = FastAPI()


@ app.get("/")
async def root():
    # Return html document
    return FileResponse('interface.html')


@ app.get("/process_allele", response_model=ProcessAlleleResponse)
async def check_allele(allele_name: str = Query(example="ura4+::pact1-cut11-mch:KanMX6", description="The name of the allele to be checked")):

    # Here is where your function would take the allele name and return the pattern
    allele_pattern = name2pattern(allele_name)

    tree_list = []
    for pattern in allele_pattern:
        tree_list.append(ParentedTree(pattern[0], pattern[1]))

    # Call the pseudo_grammar
    with open('grammar/pseudo_grammar.json') as f:
        pseudo_grammar = json.load(f)
    pseudo_grammar = post_process_pseudo_grammar(pseudo_grammar)
    input_tree = ParentedTree('ROOT', tree_list)
    output_tree = apply_pseudo_grammar(input_tree, pseudo_grammar)
    # response = ProcessAlleleResponse(
    #     name=allele_name,
    #     pattern=allele_pattern
    # )

    return HTMLResponse(TreePrettyPrinter(output_tree).svg())
