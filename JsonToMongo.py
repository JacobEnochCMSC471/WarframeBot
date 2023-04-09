#!/usr/bin/env python
# coding: utf-8

# # JSON Digestion File
# This is used to transfer many .json files into MongoDB. 

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install pymongo')
get_ipython().system('pip freeze')
from pymongo import MongoClient


# In[68]:


client = MongoClient("mongodb://localhost:27017/")
db = client['WarframeRelics']


# In[69]:


collection_list = ["Axi", "Neo", "Meso", "Lith"]


# In[70]:


axi_dir = "WFCD warframe-drop-data gh-pages data-relics/Axi"
neo_dir = "WFCD warframe-drop-data gh-pages data-relics/Neo"
meso_dir = "WFCD warframe-drop-data gh-pages data-relics/Meso"
lith_dir = "WFCD warframe-drop-data gh-pages data-relics/Lith"

relic_tiers = [axi_dir, neo_dir, meso_dir, lith_dir]


# In[71]:


import os
import json
from pathlib import Path

# Index 0 = Axi | Index 1 = Neo | Index 2 = Meso | Index 4 = Lith
filepath_lists = []

for tier in relic_tiers:
    temp_list = []
    files = Path(tier).glob('*')

    for file in files:
        temp_list.append(file)
    
    filepath_lists.append(temp_list)


# In[75]:


for index in range(4):
    curr_collection = db.get_collection(collection_list[index])
    curr_tier = filepath_lists[index]
    print(curr_collection)
    
    for relic in curr_tier:
        with open(relic) as file:
            file_json = json.load(file)
            curr_collection.insert_one(file_json)
        file.close()


# In[52]:


for item in all_paths:
    with open(item) as file:
        file_json = json.load(file)
        relic_collection.insert_one(file_json)
    file.close()

