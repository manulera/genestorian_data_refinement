set -e
for folder in *_lab;
do
    cd $folder
    if [ -f "strains.tsv" ] && [ ! -f "alleles_pattern_nltk.json" ]; then
        python ../../genestorian_module/genestorian_module/build_nltk_tags.py ./strains.tsv
        python ../../genestorian_module/genestorian_module/summary_nltk_tags.py alleles_pattern_nltk.json
    fi
    cd ..
done