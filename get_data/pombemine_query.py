import requests

query = """
<query model="genomic" view="Gene.primaryIdentifier Gene.symbol Gene.organism.species Gene.alleles.primaryIdentifier Gene.alleles.description Gene.alleles.expression" constraintLogic="(A)" sortOrder="">
   <constraint path="Gene.organism.species" value="pombe" op="=" code="A"/>
</query>
"""
query = query.strip()

response = requests.get(
    f'http://pombemine.rahtiapp.fi/pombemine/service/query/results?query={query}&format={"tsv"}&size=10'
)

print(response.status_code)
print(response._content)