import DataFrames
from collections import defaultdict


dict_koken_beidejaren = defaultdict(list)

for d in (dict_gang_vorigjaar, dict_gang_ditjaar): # you can list as many input dicts as you want here
    for key, value in d.items():
        dict_koken_beidejaren[key].append(value)
    
print(dict_koken_beidejaren)

def koken(vorig_jaar, dit_jaar):
    if vorig_jaar == dit_jaar:
        return 1
    else:
        return 0


#print(koken('Voor', 'Voor'))
