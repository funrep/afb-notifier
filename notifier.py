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

def load():
    r = requests.get(url)
    j = json.loads(r.text)
    return j

rules = {
    'area': lambda x: x not in ['Delphi', 'Sparta', 'Parantesen'],
    'sqrMtrs': lambda x: float(x) > 20,
    'numberOfReservations': lambda x: int(x) < 50,
    'rent': lambda x: int(x) < 6000,
}

def pick(p):
    for k, r in rules.items():
        if not r(p[k]):
            return False
    return True

def show(p):
    info = [
        'address',
        'area',
        'sqrMtrs',
        'numberOfReservations',
        'rent',
        # 'productId',
    ]
    s = ''
    for k in info:
        s += k + ': ' + p[k] + '\n'
    url = 'https://www.afbostader.se/lediga-bostader/bostadsdetalj/?obj=4529&area=Sparta&mode=0'
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
            print('Already notified!')
    except:
        fn = filename()
        j = None
        with open(fn, 'w') as f:
            j = load()
            f.write(json.dumps(j))
        
        msg = ''
        for p in j['product']:
            if pick(p):
                msg += show(p)
        
        today = datetime.today().strftime('%Y-%m-%d')
        subject = 'Afb report ' + today
        if len(msg) > 0:
            gmail.mail(subject, msg)

if __name__ == '__main__':
    main()
