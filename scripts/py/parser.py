# -*- coding: utf-8 -*-

import os, shutil

import ujson
from tqdm import tqdm

from scripts.py.logger import parser_logger

class DemoParser():
    def __init__(self, result: dict):
        self._matchId_short = result['matchId'].split('/')[:-2]
        self._parser_path = "scripts/go/parser.go"

    @parser_logger('parse demofile')
    def parse(self):
        demo_dir = os.path.join("demofiles", self._matchId_short)
        for demofile in tqdm(os.listdir(demo_dir)):
            if not demofile.endswith(".dem"):
                continue
            demo_path = os.path.join(demo_dir, demofile)
            os.system(f"go run {self._parser_path} --filepath '{demo_path}' --tofile temp.json")
            os.remove(demo_path)
            with open("temp.json", "r") as infile:
                parsed_json = ujson.load(infile)[1:]
                print(parsed_json)
            os.remove("temp.json")
        shutil.rmtree(demo_dir, ignore_errors=True)
