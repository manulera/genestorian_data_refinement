# Patterns

Patterns that can be found in allele descriptions, and what they mean. For now just for _S. pombe_:

* `GENE-TAG-MARKER`: This pattern corresponds to a C-terminal tagging of a protein, where a tag has been added in frame with the gene coding sequence, and a selection marker has been added after that, to be able to select the cells that incorporated the DNA fragment. See the info for tags in [biological concepts](biological_concepts.md#protein-tags). Note that after the TAG there is likely a terminator, but this information is in general omitted. The most common terminator used in S. pombe is the ADH1 terminator that comes from ADH1 gene. You can see it in this plasmid https://www.addgene.org/browse/sequence/49550/. Also note how the marker has its own promoter and terminator so that the protein that protects the cells from Kanamicin (KanR) is also expressed in the cells.
* `GENE-MARKER`: This pattern represents a deletion (typically written as gene::marker, for example les1::Hph in the Dey collection).
* `pGENE-GENE`: this in general would mean promoter of the first gene, that has been inserted in front of the second gene, replacing the original promoter of the second gene.
* `ura4+:something else`: This is a special case, not sure how common it is, you can find `ade6`, `ura4`, `lys3`, `his5` . See [integration in auxotrophy locus](biological_concepts.md#integration-in-auxotrophy-locus).

# Entities:

## Tags

* mCherry:
  * mCh

* Fluorescent proteins:
  * Green:
    * sfGFP: https://pubmed.ncbi.nlm.nih.gov/16353266/#:~:text=SFGFP%20is%20a%20novel%20and,fused%20to%20poorly%20folding%20proteins.
    * mNeonGreen
      * mNG
    * GFP: In _S. pombe_ it will often not be GFP, and be GFP(S65T) or other derivative, most likely https://www.fpbase.org/protein/gfp-s65t/ but we can name it GFP if they labelled it like that.
    * mEoS3.2: https://www.fpbase.org/protein/meos32/
  * Red:
    * mCherry: https://www.fpbase.org/protein/mcherry/
      * mCh
    * mMaple3: https://www.fpbase.org/protein/mmaple3/