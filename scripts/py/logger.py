# -*- coding:utf-8 -*-
import datetime


def parser_logger(purpose: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            cT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                print(f'[INFO] ==START== {purpose} ({cT})')
                values = func(*args, **kwargs)
                print(f'[INFO] ==END== {purpose} ({cT})')
                return values
            except Exception as ept:
                print(f'[ERROR] {purpose} | {ept} ({cT})')
                raise False
        return wrapper
    return decorator
