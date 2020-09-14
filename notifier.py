import requests
import json
import os

url = 'https://www.afbostader.se/redimo/rest/vacantproducts'
filename = 'afb.json'

def fetch():
    print('Fetching data from afb...')
    r = requests.get(url)
    with open(filename, 'w') as f:
        f.write(r.text)
    print('Saved to afb.txt')

def load():
    d = ''
    try:
        with open(filename, 'r') as f:
            d = f.read()
    except:
        fetch()
        with open(filename, 'r') as f:
            d = f.read()
    return json.loads(d)

rules = {
    'area': lambda x: x not in ['Delphi', 'Sparta', 'Parantesen'],
    'rent': lambda x: int(x) < 6000,
    'sqrMtrs': lambda x: float(x) > 20,
    'numberOfReservations': lambda x: int(x) < 50,
}

def pick(p):
    # for k, r in rules.items():
    #     if not r(p[k]):
    #         return False
    # return True
    return all([r(p[k]) for k, r in rules.items()])

def show(p):
    info = [
        'address',
        'area',
        'rent',
        'sqrMtrs',
        'floor',
        'numberOfReservations',
        # 'productId',
    ]
    s = ''
    for k in info:
        s += k + ': ' + p[k] + '\n'
    s += 'https://www.afbostader.se/lediga-bostader/bostadsdetalj/?obj=' + p['productId'] + '&area=' + p['area'] + '\n'
    s += '-----'
    return s

def process():
    j = load()
    for p in j['product']:
        if pick(p): 
            print(show(p))

if __name__ == '__main__':
    process()
