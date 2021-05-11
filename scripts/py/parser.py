# -*- coding: utf-8 -*-

import os
import shutil
from typing import Union, Dict, List

import ujson
from tqdm import tqdm

from scripts.py.logger import parser_logger


class DemoParser():
    def __init__(self, result: dict, config: dict):
        result['matchId'] = result['matchId'].split('/')[-2]
        self._matchId_short = result['matchId']
        self._parser_path = "scripts/go/parser.go"
        self._config = config
        self._header = result

    def dump_api(self, filepath: str, json_obj: Union[Dict, List]):
        with open(filepath, 'w') as apifile:
            ujson.dump(json_obj, apifile)
    
    def load_api(self, filepath: str) -> dict:
        with open(filepath, 'r') as apifile:
            return ujson.load(apifile)

    @parser_logger('parse demofile')
    def parse(self):
        demo_dir = os.path.join("demofiles", self._matchId_short)
        for demofile in tqdm(os.listdir(demo_dir)):
            if not demofile.endswith(".dem"):
                continue
            # get mapname
            mapname = demofile.split('-')[-1][:-4]
            if mapname not in self._config['map_support']:
                continue
            demo_path = os.path.join(demo_dir, demofile)
            os.system((
                f"go run {self._parser_path}"
                f" -filepath '{demo_path}'"
                " -topath 'temp.json'"
            ))
            os.remove(demo_path)

            with open("temp.json", "r") as infile:
                parsed_json = ujson.load(infile)[1:]
            os.remove("temp.json")

            res_json = {
                'header': self._header,
                'body': parsed_json
            }
            pre_dir = os.path.join('docs', mapname)
            final_dir = os.path.join(pre_dir, self._matchId_short)
            if os.path.exists(final_dir):
                shutil.rmtree(final_dir)
            os.mkdir(final_dir)
            # dump
            restored_json = self.load_api(os.path.join(pre_dir, 'index.json'))
            restored_json.append(self._header)
            self.dump_api(os.path.join(pre_dir, 'index.json'), restored_json)
            self.dump_api(os.path.join(final_dir, 'index.json'), parsed_json)


        shutil.rmtree(demo_dir, ignore_errors=True)
