# -*- coding: utf-8 -*-
import os, shutil
import datetime
from typing import Union, Dict, List

import requests
import yaml
import ujson
from tqdm import tqdm

from scripts.py.logger import parser_logger
from scripts.py.downloader import Downloader
from scripts.py.parser import DemoParser


class API_Task:
    @parser_logger('init/load config')
    def __init__(self):
        self._config = {}
        with open('config.yml', 'r', encoding='utf-8') as cfile:
            self._config = yaml.load(cfile.read(), Loader=yaml.FullLoader)

    def __convert_timeformat(self, utcTime: str) -> str:
        utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        ctime = datetime.datetime.strptime(utcTime, utc_format)
        localtime = ctime + datetime.timedelta(
            hours=float(self._config['time_format']['time_delta'])
        )
        return localtime.strftime("%Y-%m-%d %H:%M:%S")

    def request_recent_results(self) -> List:
        _url = self._config['hltv-api'] + '/api/results'
        resp = requests.get(_url)
        all_results = ujson.loads(resp.content.decode('utf-8'))
        # match filter
        if self._config['match_filter']['enable']:
            team_whitelist = self._config['match_filter']['team_whitelist']
            all_results = list(filter(
                lambda result: result['team1']['name'] in team_whitelist or
                result['team2']['name'] in team_whitelist,
                all_results
            ))[0: int(self._config['match_filter']['match_max_count'])]
        # time format change
        if self._config['time_format']['localtime']:
            for result in all_results:
                result['time'] = self.__convert_timeformat(result['time'])
                del result['team1']['crest'], result['team2']['crest']

        return all_results

    def dump_api(self, api_name: str, json_obj: Union[Dict, List]):
        with open(os.path.join('docs', api_name), 'w') as apifile:
            ujson.dump(json_obj, apifile)

    @parser_logger('fetch and parse')
    def start(self):
        all_results = self.request_recent_results()

        # create dir 'demofiles'
        demodir = 'demofiles'
        if os.path.exists(demodir):
            shutil.rmtree(demodir, ignore_errors=True)
        os.mkdir(demodir)


        for result in tqdm(all_results):
            cDownloader = Downloader(result['matchId'])
            # cDownloader.run()
            cParser = DemoParser(result['matchId'])
            # cParser.parse()

            del result['matchId']

        # delete dir 'demofiles'
        shutil.rmtree(demodir, ignore_errors=True)
        # temp
        self.dump_api('getMatches.md', all_results)
