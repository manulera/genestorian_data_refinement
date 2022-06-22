import pandas as pd
import re
import numpy as np
from collections import Counter
from Identifiers.markers import markers
from Identifiers.tags import tags

#TODO: Move these to separate files
promoters = [r'p?nmt\d*',r'p?adh\d*',r'prep\d*']
markers = ['kanr','kanmx6','kanmx4','kanmx','hygr','hyg','hphmx','hphr','hph','natmx','natr','nat','kan','natmx6',r'\d*myc',r'\d*flag\d*']
tags = ['tdtomato','megfp','egfp','gfp','mcherry','cfp','spmneongreen','mneongreen','2xyfp','myfp','yfp']

class Analyse():
    def __init__(self):
        pass
 
    def convert_to_tsv(self, in_path, out_path):
        read_file = pd.read_excel(in_path)
        read_file.to_csv(out_path, sep = '\t')
        return None
    
    def col_name(self, input_path):
        data = pd.read_csv(input_path, sep='\t')
        list1 = np.array(data.columns)
        if 'genotype' in list1:
            col_name = 'genotype'
        if 'Genotype' in list1:
            col_name = 'Genotype'
        if 'GENOTYPE' in list1:
            col_name = 'GENOTYPE'
        return col_name

    def extract_allele_names(self, input_path):
        allele_names = set([])
        usecol = self.col_name(input_path)
        data = pd.read_csv(input_path, sep = '\t', usecols= [usecol])
        data[usecol] = data[usecol].astype(str)
        for genotype in data[usecol]:
            allele_names.update([a.lower() for a in  re.split("\s+",genotype)]) 
        return allele_names
 
 
    #TO DO: divide the func to return one element at a time
    def read_gene_names(self):
        systematic_ids = set()
        gene_names = set()
        other = set()
        gene_dictionary = dict()
 
        def add_gene_name(gene_name):
            if re.match(r'[a-z]{3}\d+',gene_name) is not None:
                gene_names.add(gene_name)
            elif re.match(r'SP.+\.\d+c?',gene_name) is not None:
                systematic_ids.add(gene_name)
            else:
                other.add(gene_name)
            return None
        with open('../data/gene_IDs_names.tsv') as ins:
        # First line does not count
            ins.readline()
            for line in ins:
                fields = line.strip().split('\t')
                add_gene_name(fields[0])
                gene_dictionary[fields[0]] = fields[0]
                if len(fields)>1:
                    add_gene_name(fields[1])
                    gene_dictionary[fields[1]] = fields[0]
                    if len(fields)>2:
                        if ',' in fields[2]:
                            [add_gene_name(f) for f in fields[2].split(',')]
                            for f in fields[2].split(','):
                                add_gene_name(f)
                                gene_dictionary[f] = fields[0]
                        else:
                            add_gene_name(fields[2])
                            gene_dictionary[fields[2]] = fields[0]
        return [gene_names, gene_dictionary, systematic_ids, other]

    def create_allele_dict(self):
        allele_dictionary = dict()

        with open('../data/alleles_pombemine.tsv') as ins:
            for line in ins:
                ls = line.strip().split('\t')
                if 'delta' not in ls[2]:
            # Check if the key already exists, if not create a list with that value
                    systematic_id = ls[0]
                    allele_name = ls[2]
                    if systematic_id in allele_dictionary:
                        allele_dictionary[systematic_id].append(allele_name)
            # Otherwise, append to the existing list
                    else:
                        allele_dictionary[systematic_id] = [allele_name]

        # All lists of alleles should be order in inverse order of length, so that you try to subsitute the longest names first,
        for key in allele_dictionary:
            allele_dictionary[key].sort(key=len,reverse=True)
        return allele_dictionary

    
    def replace_entity(self, alleles_with_replaced_name, identifiers, IDENTIFIER):
        for i in range(len(alleles_with_replaced_name)):
            for identifier in identifiers:
                alleles_with_replaced_name[i]=re.sub(identifier, IDENTIFIER, alleles_with_replaced_name[i])
        return alleles_with_replaced_name



    def replace_allele_names(self):
        print('def')
        alleles_with_replaced_name = []
        allele_names  = self.extract_allele_names()

        gene_info = self.read_gene_names()
        gene_names = gene_info[0] 
        gene_dictionary = gene_info[1]
        systematic_ids = gene_info[2]

        allele_dictionary = self.create_allele_dict()
        for genotype_allele in allele_names:
            for name in re.findall(r'[a-z]{3}\d+',genotype_allele):
                if name in gene_names:
                    # Get the systematic id of the gene
                    systematic_id = gene_dictionary[name]

                    # Find the alleles of that gene and see if any of them is in the alelle name
                    allele_found = False
                    if systematic_id in allele_dictionary:
                        for published_allele in allele_dictionary[systematic_id]:
                            if published_allele.lower() in genotype_allele:
                                genotype_allele = genotype_allele.replace(published_allele.lower(),'ALLELE')
                                allele_found = True
                                break

                    # If the allele name was not found, replace with GENE
                    if not allele_found:
                        genotype_allele = genotype_allele.replace(name,'GENE')

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
       
            alleles_with_replaced_name.append(genotype_allele)
        
        #replace markers, tags and promoters
        alleles_with_replaced_name = self.replace_entity(alleles_with_replaced_name,markers, 'MARKER')
        alleles_with_replaced_name = self.replace_entity(alleles_with_replaced_name,tags, 'TAG')
        alleles_with_replaced_name = self.replace_entity(alleles_with_replaced_name,promoters, 'PROMOTER')


        #replace the white spcaes with a single dash, a leading or trailing symbol
        for i in range(len(alleles_with_replaced_name)):
            alleles_with_replaced_name[i] = re.sub(r'[:-<\.]+','-',alleles_with_replaced_name[i])
            alleles_with_replaced_name[i] = re.sub(r'^-','',alleles_with_replaced_name[i])
            alleles_with_replaced_name[i] = re.sub(r'-$','',alleles_with_replaced_name[i])

        return alleles_with_replaced_name

    def identify_common_pattern(self):
        alleles_with_replaced_name = self.replace_allele_names()
        print('abc')
        counted = Counter(alleles_with_replaced_name)
        # Sort
        result = counted.most_common()

        # Write into file
        with open('dummy00.txt','w', encoding = 'utf-8') as out:
            for r in result:
                out.write(f'{r[0]} {r[1]}\n')
        return None    

def count_most_common_consecutive_N_characters(file, n):
    all_occurrences = list()
    with open(file,'r', encoding = 'utf-8') as ins:
        for line in ins:
            line = line.strip()
            line = line.replace('GENE','')
            line = line.replace('MARKER','')
            line = line.replace('TAG','')
            line = line.replace('ALLELE','')
            line = line.replace('PROMOTER','')
            if len(line)>=n:
                all_occurrences += [line[i:i+  n] for i in range(0,len(line)-n+1)]

    return Counter(all_occurrences)  

def find(text, file):
    occurences = []
    with open(file,'rt') as ins:
        usecol = Analyse().col_name(file)
        data = pd.read_csv(ins, sep='\t', usecols = [usecol])
        data[usecol] = data[usecol].astype(str)
        for genotype in data[usecol]:
            if text in genotype.lower(): # if the username shall be on column 3 (-> index 2)
                occurences.append(genotype)
    
    return occurences






        

         
