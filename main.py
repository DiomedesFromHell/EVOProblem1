import string
import re

from functools import reduce  # forward compatibility for Python 3
import operator
DATA = {
    'languages': {
        'python': {
            'latest_version': '3.6',
            'site': 'http://python.org',
        },
        'rust': {
            'latest_version': '1.17',
            'site': 'https://rust-lang.org',
        },
    },
    'animals': ['cow', 'penguin'],
    'crew': 1
}

template = ('Python version: {languages[python][latest_version]}\n'
            'Python site: {languages[python][site]}\n'
            'Rust version: {languages[rust][latest_version]}\n')


def get_value(data, path):
    return reduce(operator.getitem, path, data)


def parse_path(path):
    res = []
    res.append(path.split('[', 1)[0])
    res.extend(re.findall("\[(.*?)\]", path))
    return res


def optimize_data(template, data):
    paths = [parse_path(c[1]) for c in string.Formatter().parse(template) if c[1] is not None]
    res = {}
    for item in paths:
        add_path(res, item, data)
    return res


def add_path(dict, path, data):
    k = -1
    d = dict
    if isinstance(get_value(data, path[:-1]), list):
        k = -2
    for i, item in enumerate(path[:k]):
        # if i == len(path) - 1:
        #     d[item] = get_value(data, path)
        if item not in d:
            d[item] = {}
        d = d[item]
    if k == -1:
        leaf = path[len(path) - 1].split('.')
        if len(leaf) == 1:
            d[path[len(path) - 1]] = get_value(data, path)
        elif len(leaf) == 2:
            path[len(path) - 1] = leaf[0]
            d[path[len(path) - 1]] = get_value(data, path)
    if k == -2:
        lst = [None] * len(get_value(data, path[:-1]))
        lst[int(path[len(path) - 1])] = get_value(data, path[:-1])[int(path[len(path) - 1])]
        d[path[len(path) - 2]] = lst



