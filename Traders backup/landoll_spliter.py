import re, datetime, sys, os, time
from unidecode import unidecode
import requests, json, time
from ordered_set import OrderedSet


file = "/Users/atulsmac/PycharmProjects/pythonBots/removeDups.json"
f = open(file)
data = json.load(f)
# print(data)
Unique_data=[]

for nodes in data:
    # print(nodes)
    nod=nodes["general"]["category"]
    if nod=="Trailers":
      pass
    else:
        Unique_data.append(nodes)
        # print(nodes)
with open('Landoll_other2020-11-20.json', 'w') as f:
    json.dump(Unique_data,f)


