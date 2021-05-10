# -*- coding: utf-8 -*-

import os
import shutil

import requests
from bs4 import BeautifulSoup

from scripts.py.logger import parser_logger


class Downloader():
    def __init__(self, result: dict):
        self._matchId_long = result['matchId']
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

    def get_demoId(self) -> str:
        url = f"https://hltv.org{self._matchId_long}"
        resp = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
        links = list(filter(
            lambda x: 'download/demo' in x['href'],
            soup.findAll('a')
        ))
        assert len(links) > 0, f'demoId not found by {self._matchId_short}'
        return links[0]['href']

    def download(self, demoId: str) -> bool:
        url = f"https://hltv.org{demoId}"
        resp = requests.get(url, headers=self._headers, stream=True)
        if resp.status_code != requests.codes.ok:
            return False

        file_size_bytes = float(resp.headers['Content-Length'])
        rar_path = os.path.join("demofiles", f"{self._matchId_short}.rar")
        print(f"[INFO] <{rar_path}> {file_size_bytes}bytes")
        with open(rar_path, 'ab') as demoFile:
            for chunk in resp.iter_content(chunk_size=1024):
                if not chunk:
                    continue
                demoFile.write(chunk)
                demoFile.flush()
        return True

    def unrar(self):
        export_dir = os.path.join("demofiles", self._matchId_short)
        if os.path.exists(export_dir):
            shutil.rmtree(export_dir, ignore_errors=True)
        os.mkdir(export_dir)
        os.system(f"unrar x {export_dir}.rar {export_dir}")
        os.remove(f"{export_dir}.rar")

    @parser_logger('fetch demoId and downloading')
    def run(self):
        demoId = self.get_demoId()
        print(f'MatchId: {self._matchId_short}, DemoId: {demoId}')
        if self.download(demoId):
            self.unrar()
