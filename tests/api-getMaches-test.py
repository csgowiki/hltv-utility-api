# -*- coding: utf-8 -*-
import requests


def main():
    url = "https://api.hx-w.top/getMatches.json"
    resp = requests.get(url)
    print(resp.content.decode('utf-8'))


if __name__ == '__main__':
    main()
