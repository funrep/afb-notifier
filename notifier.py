import requests
import json
import os
from datetime import datetime

import gmail

url = 'https://www.afbostader.se/redimo/rest/vacantproducts'

def filename():
    # Directory path of this file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    today = datetime.today().strftime('%Y-%m-%d')
    return dir_path + '/afb' + today + '.json'

def fetch():
    print('Fetching data from afb...')
    r = requests.get(url)
    fn = filename()
    with open(fn, 'w') as f:
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
    s += '-----\n'
    return s

def process():
    j = load()
    for p in j['product']:
        if pick(p): 
            print(show(p))

def main():
    try:
        fn = filename()
        with open(fn, 'r') as _:
            print('Already notified today!')
            return
    except:
        fetch()
        d = ''
        with open(fn, 'r') as f:
            d = f.read()
        j = json.loads(d)

        msg = ''
        for p in j['product']:
            if pick(p):
                msg += show(p)

        # print(msg)
        subject = 'Afb report ' + datetime.today().strftime('%Y-%m-%d')
        gmail.mail(subject, msg)

if __name__ == '__main__':
    # process()
    main()
