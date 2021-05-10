# -*- coding: utf-8 -*-

import requests


def main():
    url = 'https://api.hx-w.top/de_dust2'
    resp = requests.get(url).content.decode('utf-8')
    print('size:', len(resp))
    print(resp)

if __name__ == '__main__':
    main()
