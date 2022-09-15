# %%

from nltk.chunk.regexp import RegexpChunkRule, ChunkString
import re
from nltk.tree import Tree
from nltk.chunk import RegexpParser
# %%
grammar = """
    GENE_DELETION|BLAH: {<GENE><SPACER>?<other>?<SPACER>?<MARKER>}
"""

custom_tag_parser = RegexpParser(grammar, root_label='ROOT')

input = Tree('ROOT', [
    Tree('GENE', ['mph1']),
    Tree('SPACER', ['::']),
    Tree('other', ['hello']),
    Tree('SPACER', ['::']),
    Tree('MARKER', ['kanr'])
])
result: Tree = custom_tag_parser.parse_all(input)
# custom_tag_parser

# %%

# match = re.match('(aa)aa', 'aaaa')
# match.group()
# %%
cs = ChunkString(input)

rule = RegexpChunkRule.fromstring(
    '{<GENE><SPACER>?<other>?<SPACER>?<MARKER>}')

print(rule._regexp)

match = re.match(rule._regexp, cs._str)
print(rule._regexp)
print(match.groups())
# cs.xform(rule._regexp, '{\g<chunk>}')
rule._regexp.flags
# print(cs._str)
