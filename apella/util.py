from os import path
import re


def urljoin(*args):
    return path.join(args[0], *map(lambda x: x.lstrip('/'), args[1:]))


def safe_path_join(base, path, sep=path.sep):
    safe_path = sep.join(x for x in path.split(sep) if x and x != '..')
    return base.rstrip(sep) + sep + safe_path
