import json
import sys
import operator
from pprint import pprint

with open('bills.json') as openFile:
    data = json.load(openFile)

sorted_bills = sorted(data, key=lambda k: k['synset_change'], reverse=True)
pprint(sorted_bills)
