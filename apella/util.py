from os import path

def urljoin(*args):
    return path.join(args[0], *map(lambda x: x.lstrip('/'), args[1:]))

