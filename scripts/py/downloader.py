# -*- coding: utf-8 -*-

import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

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

    def download(self) -> bool:
        url = f"https://hltv.org{self._demoId}"
        resp = requests.get(url, headers=self._headers, stream=True)
        if resp.status_code != requests.codes.ok:
            return False

        file_size_bytes = float(resp.headers['Content-Length'])
        rar_path = os.path.join("demofiles", f"{self._matchId_short}.rar")
        print(f"[INFO] <{rar_path}> {file_size_bytes}bytes")
        with open(rar_path, 'ab') as demoFile:
            for chunk in tqdm(resp.iter_content(chunk_size=1024)):
                if not chunk:
                    continue
                demoFile.write(chunk)
                demoFile.flush()
        return True

    @parser_logger('fetch demoId and downloading')
    def start(self):
        self.get_demoId()
        print(f'MatchId: {self._matchId_short}, DemoId: {self._demoId}')
        if self.download():
            pass
