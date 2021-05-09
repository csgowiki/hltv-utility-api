# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from scripts.py.logger import parser_logger


class Downloader():
    def __init__(self, matchId_long: str, config: dict):
        self._matchId_long = matchId_long
        self._config = config
        self._headers = {
            'User-Agent': (
                'Mozilla/5.0 '
                '(iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                'Version/13.0.3 Mobile/15E148 Safari/604.1'
            ),
            'Referer': f'https://hltv.org{self._matchId_long}'
        }
        self._matchId_short = self._matchId_long.split('/')[-2]
        self._demoId = False

    def get_demoId(self):
        url = f"https://hltv.org{self._matchId_long}"
        resp = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
        links = list(filter(
            lambda x: 'download/demo' in x['href'],
            soup.findAll('a')
        ))
        assert len(links) > 0, f'demoId not found by {self._matchId_short}'
        self._demoId = links[0]['href']

    @parser_logger('fetch demoId and downloading')
    def start(self):
        self.get_demoId()
        print(f'MatchId: {self._matchId_short}, DemoId: {self._demoId}')
