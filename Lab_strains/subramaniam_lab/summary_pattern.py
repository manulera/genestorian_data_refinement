
from genestorian_module.summary_nltg_tags import (json_common_pattern_dict,
                                                  count_common_patterns,
                                                  count_most_common_other_tag)

json_common_pattern_dict('alleles_nltk.json')
count_common_patterns('alleles_nltk.json')
count_most_common_other_tag('alleles_nltk.json')
