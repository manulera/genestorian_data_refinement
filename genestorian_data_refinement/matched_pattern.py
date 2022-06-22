import re
import pandas as pd
import json
from pattern_identify import Analyse




class Matched_Patterns(Analyse):
    def __init__(self):
        pass
    def matched_patterns(self, in_path):
        allele_names = Analyse().extract_allele_names(in_path)
        gene_names, gene_dictionary, systematic_ids, other = Analyse().read_gene_names()
        allele_dictionary = Analyse().create_allele_dict()
        tags, markers, promoters = Analyse().load_identifiers()
        pattern_dict = {}
        for genotype_allele in allele_names:
            Genotype_allele = genotype_allele
            for name in re.findall(r'[a-z]{3}\d+',genotype_allele):
                if name in gene_names:

                 # Get the systematic id of the gene
                    systematic_id = gene_dictionary[name]
                    allele_found = False
                    if systematic_id in allele_dictionary:
                        for published_allele in allele_dictionary[systematic_id]:
                            if published_allele.lower() in genotype_allele:
                                genotype_allele = genotype_allele.replace(published_allele.lower(),'ALLELE')
                                #print(genotype_allele)
                                allele_found = True
                                break
                                # If the allele name was not found, replace with GENE
                    if not allele_found:
                        genotype_allele = genotype_allele.replace(name,'GENE')

            # Here no caps, because we have changed all genotypes to no caps
            for systematic_id in re.findall(r'sp.+\.\d+c?',genotype_allele):
                if systematic_id in map(str.lower, systematic_ids):
                    allele_found = False
                    if systematic_id in allele_dictionary:
                        for published_allele in allele_dictionary[systematic_id]:
                            if published_allele.lower() in genotype_allele:
                                genotype_allele = genotype_allele.replace(published_allele.lower(),'ALLELE')
                                allele_found = True
                                break
            
                    # If the allele name was not found, replace with GENE
                    if not allele_found:
                        genotype_allele = genotype_allele.replace(systematic_id,'GENE')
            for marker in markers:
                genotype_allele = re.sub(marker,'MARKER',genotype_allele)

            for tag in tags:
                genotype_allele = re.sub(tag,'TAG',genotype_allele)

            for promoter in promoters:
                genotype_allele = re.sub(promoter,'PROMOTER',genotype_allele)


            genotype_allele = re.sub(r'[:-<\.]+','-', genotype_allele)
            genotype_allele = re.sub(r'^-','', genotype_allele)
            genotype_allele = re.sub(r'-$','',genotype_allele)




            if genotype_allele not in pattern_dict.keys():
                pattern_dict.update({ genotype_allele: [Genotype_allele]})
            else:
                pattern_dict.setdefault(genotype_allele).append(Genotype_allele)
        return pattern_dict

    def find_pattern(self, in_path , pattern):
        pattern_dict = self.matched_patterns(in_path)
        if pattern in pattern_dict.keys():
            return pattern_dict.get(pattern)

    def same_pattern_genotype(self, in_path, output_path, pattern):
        pattern_dict = self.find_patter(in_path, pattern)
        with open(output_path, 'w') as fp:
            json.dump(pattern_dict, fp, indent=3)
        return None

    def json_similar_pattern_file(self, in_path, output_path):
        pattern_dict = self.matched_patterns(in_path)
        with open(output_path, 'w') as fp:
            json.dump(pattern_dict, fp, indent=3)
        return None
