# -*- coding: utf-8 -*-
import requests


def main():
    url = 'https://hx-w.github.io/hltv-utility-api/getMatches.json'
    resp = requests.get(url)
    print(resp.content.decode('utf-8'))


if __name__ == '__main__':
    main()
