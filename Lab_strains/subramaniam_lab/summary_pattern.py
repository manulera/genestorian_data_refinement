from genestorian_module.summary_nltg_tags import json_common_pattern_dict, count_common_patterns, count_most_common_other_tag

json_common_pattern_dict('alleles_nltk.json', 'occurrence_nltk.json')
count_common_patterns('alleles_nltk.json', 'common_pattern_count.txt')
count_most_common_other_tag('alleles_nltk.json','most_common_other_tag')