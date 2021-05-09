# -*- coding: utf-8 -*-

from scripts.py.match_detector import API_Task

def start():
    task = API_Task()
    print(task.get_config())


if __name__ == '__main__':
    start()
