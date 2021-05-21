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

    def json_fix(self, pjson: list) -> list:
        float_index = [0, 1, 2, 3, 4, 5, 10, 14, 15, 16, 18, 19, 20, 21, 22, 23]
        int_index = [9]
        for item_idx in range(len(pjson)):
            for float_ in float_index:
                pjson[item_idx][float_] = float(pjson[item_idx][float_])
            for int_ in int_index:
                pjson[item_idx][int_] = int(pjson[item_idx][int_])
        return pjson


    @parser_logger('parse demofile')
    def parse(self):
        demo_dir = os.path.join("demofiles", self._matchId_short)
        for demofile in tqdm(os.listdir(demo_dir)):
            if not demofile.endswith(".dem"):
                continue
            # get mapname
            mapname = "de_" + demofile.split('-')[-1][:-4]
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
            parsed_json = self.json_fix(parsed_json)

            if len(parsed_json) == 0:
                continue
            pre_dir = os.path.join('docs', mapname)
            final_dir = os.path.join(pre_dir, self._matchId_short)
            if os.path.exists(final_dir):
                shutil.rmtree(final_dir)
            os.mkdir(final_dir)
            # dump
            restored_json = self.load_api(os.path.join(pre_dir, 'index.json'))
            # find maxround
            for s_json in parsed_json:
                self._header['maxround'] = max(0, int(s_json[9]))
            restored_json.append(self._header)
            self.dump_api(os.path.join(pre_dir, 'index.json'), restored_json)
            self.dump_api(os.path.join(final_dir, 'index.json'), parsed_json)

            round_map = []
            for item in parsed_json:
                cround = int(item[9])
                if len(round_map) < cround:
                    round_map.append([item])
                else:
                    round_map[cround - 1].append(item)

            for round_int in range(0, self._header['maxround']):
                round_dir = os.path.join(final_dir, f'round{round_int + 1}')
                if os.path.exists(round_dir):
                    shutil.rmtree(round_dir)
                os.mkdir(round_dir)
                self.dump_api(os.path.join(round_dir, 'index.json'), round_map[round_int])

        shutil.rmtree(demo_dir, ignore_errors=True)
