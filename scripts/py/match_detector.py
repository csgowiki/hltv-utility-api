# -*- coding: utf-8 -*-

import requests
import yaml

class API_Task:
    def __init__(self):
        self._config = {}
        with open('config.yml', 'r', encoding='utf-8') as cfile:
            self._config = yaml.load(cfile.read(), Loader=yaml.FullLoader)

    def get_config(self):
        return self._config
