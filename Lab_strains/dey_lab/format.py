import re
import pandas as pd


read_file = pd.read_excel('Manu_Strains.xlsx', usecols=[
                          'Sample Name', 'Genotype'])
read_file.to_csv('strains.tsv', sep='\t')

