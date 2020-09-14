import requests
import json
import os

url = 'https://www.afbostader.se/redimo/rest/vacantproducts'

def process():
    j = load()
    for p in j['product']:
        if pick(p): 
            print(show(p))

if __name__ == '__main__':
    # process()
