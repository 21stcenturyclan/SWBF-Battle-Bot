import json
import operator
import os
import sys
from datetime import datetime
from typing import Union


def get_key(name: str):
    os.getenv(name)


def get_keys_from_ini_file(file: str, sep: str = '='):
    keys = {}
    for line in open(file, 'r').read().split('\n'):
        if line.find(sep) >= 0:
            key, value = line.split(sep)
            keys[key.strip()] = value.strip()
    return keys


def get_key_from_ini_file(name: str, file: str, sep: str = '='):
    keys = get_keys_from_ini_file(file, sep)
    return keys[name] or None


def get_key_from_file(file):
    return open(file, 'r').read()


def get_config_from_json(file: str):
    return json.load(open(file, 'r'))


def log(*msg):
    print(*msg)
    sys.stdout.flush()


def check_date(date: str):
    comp = date.split(' ')

    if not comp:
        return False

    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year
    hour = now.hour
    minute = now.minute

    if len(comp) > 0:
        if comp[0].find(':') >= 0:
            hour, minute = map(int, comp[0].split(':'))
        elif len(comp) > 1 and comp[1].find(':')  >= 0:
            hour, minute = map(int, comp[1].split(':'))

    if len(comp) > 1:
        if comp[0].find('.') >= 0:
            d_comp = comp[0].split('.')

        elif comp[1].find('.') >= 0:
            d_comp = comp[1].split('.')

        else:
            return False

        if len(d_comp) > 2:
            day, month, year = map(int, d_comp)
        elif len(d_comp) > 1:
            day, month = map(int, d_comp)
        else:
            return False

    return datetime(year, month, day, hour, minute)


def prime_factors(n: int):
    factor_list = []
    i = 2
    while n >= i:
        if n % i:
            i += 1
        else:
            factor_list.append(i)
            n /= i
    return factor_list


def number_of_factors(n: int, factors: list):
    factor_list = []
    for f in factors:
        factor_list.append(int(n / (f * 2)))
    return factor_list


def remove_from_list(l: Union[list, set], element):
    if element in l:
        l.remove(element)


def get_max(d: dict):
    return max(d.items(), key=operator.itemgetter(1))
