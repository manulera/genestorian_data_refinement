#!/usr/bin/env python
# coding: utf-8

# In[3]:


from converge import converge
converge().converge_files('converged_patterns.txt')


# In[7]:


from pattern_identify import count_most_common_consecutive_N_characters
counted = count_most_common_consecutive_N_characters('converged_patterns.txt', 10 )


# In[1]:


from pattern_identify import find
found = find('mch', '..\Lab_strains\dey_lab\Manu_strains.tsv')


# In[1]:


from matched_pattern import Matched_Patterns
Matched_Patterns().json_similar_pattern_file('..\Lab_strains\dey_lab\Manu_strains.tsv' , '..\Lab_strains\dey_lab\Manu_strains.json')


