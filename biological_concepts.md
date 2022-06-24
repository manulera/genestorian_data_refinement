# Biological concepts

A list of biological concepts important to understand the project.

## Added 27/05/2022

* DNA sequences, protein sequences (what are nucleotides and aminoacids)
* What are DNA, RNA, proteins and how sequences of DNA are replicated, transcribed and translated.
	* Transcription
	* mRNAs (messenger RNA)
	* Translation
	* tRNAs
	* Ribosomes, genetic code, start codon, stop codon, missense mutations, nonsense mutations, etc. (https://en.wikipedia.org/wiki/Genetic_code). Don't really need to remember the names, just getting the point.
* What are genes, what are promoters
* What are oligonucleotides and plasmids
* What are resistance makers / selectable markers / auxotrophy: https://en.wikipedia.org/wiki/Selectable_marker#:~:text=Selectable%20markers%20are%20often%20antibiotic,resistance%20to%20an%20antibiotic.).
* Fluorescent proteins and protein tagging
* Yeast mating
* Some molecular cloning:
	* Restriction and ligation
	* PCR
	* Crispr
	* Homologous recombination and how it is used to edit genomes. This is still the most common way of doing it in pombe, so probably worth looking at the publications that explain the principles 
	https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-0061(199807)14:10%3C943::AID-YEA292%3E3.0.CO;2-Y
	https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3190138/ (this paper has a very nice figure)
	
* About S. pombe / fission yeast, the model organism that we cover in Pombase. A lot of what you learn in here would be useful for other yeasts as well. A good place to start is this website: https://dornsife.usc.edu/pombenet/ Check the 'About Pombe' and 'working with pombe' sections. They cover the basics of how strains are generated. A very important thing to realise is that pombe is typically haploid, but sometimes diploid. A lot of eukaryotes (including ourselves) are diploid (have two copies of each gene), but most yeast strains are not like that.


Other things for the future (don't look at them yet):
* Leu2 plasmid in pombe (very specific to pombe)

## Allele components

### Protein Tags

* Common in labs that do microscopy, biochemistry or study physical interactions of proteins.
* Tagging a gene consists of the addition of a DNA fragment that codes a "protein tag". When the gene is transcribed, the tag fragment gets transcribed as well and it is added to the mRNA.
* When the mRNA is translated the tag is also translated, so the resulting protein contains an additional chunk that we call 'tag'.
* Some important things that might not be obvious:
  * Tags can be at the N-terminus (before the coding sequence of the gene starts) or after the C-terminus of the protein (after the coding sequence of the gene ends). Sometimes they are in the middle, but that's very rare.
  * Typically, in _S. pombe_ most tags are added at the C-term. The reason for it is that it is very easy to do it genetically, we can amplify a fragment from a plasmid, and integrate it into the genome after the gene coding sequence, and that's it! See below.
  ![](images/tagging.svg)
  * Some extra things: Note that the gene coding sequence would normally end in a [stop codon](https://en.wikipedia.org/wiki/Stop_codon). In order for the tag to be translated and added to the protein, when we tag a gene we remove the stop codon.
  * The tag DNA sequence has to be in-frame with the gene coding sequence. Since mRNA is translated to proteins by reading triplets (sets of three consecutive RNA nucleotides) in the ribosome, if you want to add a protein sequence, the triplets of your tag have to be in frame with the triplets of the gene coding sequence.
* Some typical tags:
  * Fluorescent tags: Like mCherry, GFP, etc. They are fluorescent and allow researchers to see proteins in a fluorescent microscope.
  * Tags used for protein purification: Some protein tags are commonly used because they can bind to an antibody or molecule. This can be used for [protein purification](https://en.wikipedia.org/wiki/Protein_purification). Basically, you extract all proteins from the cell, you pass them through a column that contains the antibody or molecule that binds to the protein tag. In principle, all the other proteins will pass through the column, but your tagged protein will stick in the column, then you can elute it with some solution that disrupts the binding. Typical examples of these kinds of tags are [the his tag](https://en.wikipedia.org/wiki/Protein_purification), [the GST tag](https://en.wikipedia.org/wiki/Glutathione_S-transferase#GST-tags_and_the_GST_pull-down_assay), [the myc tag](https://en.wikipedia.org/wiki/Myc-tag). Even fluorescent tags can be used for this, as there are antibodies against GFP or other common fluorescent tags.

## Genetic engineering

### Integration in auxotrophy locus

See [this article](https://journals.biologists.com/jcs/article/133/1/jcs240754/224748/A-toolbox-of-stable-integration-vectors-in-the) for more detail.

The idea here is to introduce a fragment of DNA in a place in the genome without disrupting an existing gene of interest. Some use-cases can be:

* We want to express a protein that does not exist in the cell.
* We want to express a variant of a protein (a fragment of it, or a mutated version) in the presence of the wild-type gene.

For this we can use an [auxotrophy locus](https://en.wikipedia.org/wiki/Auxotrophy). Basically, the locus of a gene without which cells cannot make a certain molecule that they need to live. For example, the gene `ura4` is required to produce the aminoacid uracil. If we grow cells that have their `ura4` gene mutated in a medium with uracil, they will grow, but if we remove the uracil from the medium they will die. Therefore, it can be used as a selection marker.

There are two ways of doing this, based on a similar principle. We have to start from an auxotroph strain, for example containing a mutation in `ura4` (mutant allele `ura4-294` in this example). The idea is to insert a fragment of DNA in the `ura4` locus that will restore the wild-type gene sequence of `ura4`, but will also introduce a fragment of DNA that we are interested in. There are two ways of doing these (ilustrated in the picture below) using two different plasmids:

* using pJK210: This is the "old way", in the panel A of the figure. Essentially they have a plasmid that contains the wild-type sequence of ura4, as well as the DNA seuqence that you want to insert (gray arrows in the figure). In this first case, you cut the plasmid in the middle of ura4, and this will insert in the genome by homologous recombination, generating a wild-type copy of the gene and the same ura4-294 that was already there, with whatever was in the plasmid in the middle. The problem with this method is that it can lead to multiple insertions
* using pUra4AfeI: This is the new way. Instead if cutting ura4 in the middle, the plasmid is designed so that it contains homologous fragments to two regions: the entire ura4 gene, and a donwstream fragment that they call 3'' in the picture, now the plasmid content gets integrated between 3' and 3'', and this can only happen once, preventing multiple insertions.

> **NOTE:** important not to confuse this with alleles that may say something like `ase1::ura4+`. This is a deletion of ase1. What the authors have done is to replace the `ase1` locus with the wild-type gene of `ura4`. This is likely done in a strain that has a mutation in the ura4 locus, and therefore one can select for cells deleted for ase1 by growing cells in the absence of `ase1`. If the genotype was correct, it should say something like `ase1::ura4+ ura4-294`, because the resulting strain has ura4 mutated in the ura4 locus, and a wild-type copy of it in the ase1 locus. However, researchers often ommit auxotrophies in the genotype.

![](https://cob.silverchair-cdn.com/cob/content_public/journal/jcs/133/1/10.1242_jcs.240754/3/m_jcs24075401.png?Expires=1657917517&Signature=VyDBwBw8Ra1G5aY9pnQZRoYYcNlApuyJzQUnvayNAaQEIqki2z24ezXKqqXC4oRb6cWQjcHwk4Uf2awIfKGmwJGYNp94hWgNyn7S29~awnrL--cT-qGxcnr913-mm4IiTF1zuyjumVU2c77XBdOvSlnj3DMzHn4QpBBnZtDF1SanJYyhGmcf2YmIljjhEs4kt03lm07yYvB4D1dUIIdANobAuEZeJWY1AkHy1-RYEKpEpN1kRjvhLYfV2zlM5ps1hmcSgbQauwmGCYLtDWp3nQNlhUw1zIupcS8lwZf8JyQFQzkDvZqb8y6wkUhIHs4C3f10NcLxGm8uIQddaX9xTQ__&Key-Pair-Id=APKAIE5G5CRDK6RD3PGA)