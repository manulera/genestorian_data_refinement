#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
read_file  = pd.read_excel('MBYstrains-01.xlsx' )
read_file.to_csv('MBYstrains-01.tsv', sep='\t') 


# In[2]:


import pandas
import re

# We make a set to store the alleles
allele_names = set([])
data = pandas.read_csv('MBYstrains-01.tsv', sep='\t', usecols = ['GENOTYPE'])

# We force conversion to string, otherwise empty values are parsed as nans (floats)
data['GENOTYPE'] = data['GENOTYPE'].astype(str)
for genotype in data.GENOTYPE:
    # split the genotype by any separator and add the alleles names to the set
    allele_names.update([a.lower() for a in  re.split("\s+",genotype)])


# In[3]:


# Read all gene names and identifiers

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

with open('../../data/gene_IDs_names.tsv') as ins:
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


# In[4]:


allele_dictionary = dict()

with open('../../data/alleles_pombemine.tsv') as ins:
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
# for instance, you should try to replace cdc2-12 before cdc2-1

for key in allele_dictionary:
    allele_dictionary[key].sort(key=len,reverse=True)


# In[5]:


alleles_with_replaced_name = list()
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

    alleles_with_replaced_name.append(genotype_allele)


# In[6]:


markers = ['kanr','kanmx6','kanmx4','kanmx','hygr','hyg','hphmx','hphr','hph','natmx','natr','nat','kan','natmx6',r'\d*myc',r'\d*flag\d*']

for i in range(len(alleles_with_replaced_name)):
    for marker in markers:
        alleles_with_replaced_name[i] = re.sub(marker,'MARKER',alleles_with_replaced_name[i])

tags = ['tdtomato','megfp','egfp','gfp','mcherry','cfp','spmneongreen','mneongreen','2xyfp','myfp','yfp']

for i in range(len(alleles_with_replaced_name)):
    for tag in tags:
        alleles_with_replaced_name[i] = re.sub(tag,'TAG',alleles_with_replaced_name[i])

# TODO: ask about adh promoter to authors, also prep81 and so probably wrongly used
promoters = [r'p?nmt\d*',r'p?adh\d*',r'prep\d*']

for i in range(len(alleles_with_replaced_name)):
    for promoter in promoters:
        alleles_with_replaced_name[i] = re.sub(promoter,'PROMOTER',alleles_with_replaced_name[i])


# In[7]:


for i in range(len(alleles_with_replaced_name)):
    alleles_with_replaced_name[i] = re.sub(r'[:-<\.]+','-',alleles_with_replaced_name[i])
    alleles_with_replaced_name[i] = re.sub(r'^-','',alleles_with_replaced_name[i])
    alleles_with_replaced_name[i] = re.sub(r'-$','',alleles_with_replaced_name[i])


# In[8]:


from collections import Counter

counted = Counter(alleles_with_replaced_name)
# Sort
result = counted.most_common()

# Write into file

with open('pattern_identification.txt','w', encoding = 'utf-8') as out:
    for r in result:
        out.write(f'{r[0]} {r[1]}\n')

print('reduced by',1-len(result)/len(allele_names))


# In[9]:


def count_most_common_consecutive_N(file,n):
    all_occurrences = []
    with open(file,'r', encoding = 'utf-8') as ins:
        for line in ins:
            line = line.strip()
            line = line.replace('GENE','')
            line = line.replace('MARKER','')
            line = line.replace('TAG','')
            line = line.replace('ALLELE','')
            line = line.replace('PROMOTER','')
            if len(line)>=n:
                all_occurrences += [line[i:i+ n] for i in range(0,len(line)-n+1)]
    return Counter(all_occurrences)

counted = count_most_common_consecutive_N('pattern_identification.txt',10)

with open('identifiers_replaced.txt','w', encoding = 'utf8') as out:
    for r in counted.most_common():
        out.write(f'{r[0]} {r[1]}\n') 

