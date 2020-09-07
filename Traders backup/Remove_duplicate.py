import re, datetime, sys, os, time
from unidecode import unidecode
import requests, json, time

file = "/Users/atulchaudhary/PycharmProjects/Headless/BobCatTestCode.json"
f = open(file)
data = json.load(f)
def remove_dupe_dicts(l):
  list_of_strings = [json.dumps(d, sort_keys=True)for d in l]
  list_of_strings = set(list_of_strings)
  return [json.loads(s)for s in list_of_strings]

remove_dupe_dicts(data)
