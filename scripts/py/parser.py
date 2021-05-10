# -*- coding: utf-8 -*-

import os, shutil

import ujson
from tqdm import tqdm

from scripts.py.logger import parser_logger

class DemoParser():
    def __init__(self, matchId_long: str):
        self._matchId_short = matchId_long.split('/')[:-2]
        self._parser_path = "scripts/go/parser.go"

    @parser_logger('parse demofile')
    def parse(self):
        demo_dir = os.path.join("demofiles", self._matchId_short)
        for demofile in tqdm(os.listdir(demo_dir)):
            if not demofile.endswith(".dem"):
                continue
            demo_path = os.path.join(demo_dir, demofile)

        pass
