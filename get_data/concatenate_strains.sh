for file in strains??.tsv
do
    echo $file
	ed -s $file <<< w
done

# Columns: request	PMID	Ref	NBRPID	strain_name	genotype	phenotype	source	terms	LMO	stock	comment1	comment2

cat strains??.tsv > strains.tsv
