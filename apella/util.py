from os import path
from django.conf import settings
from pytz import timezone
from datetime import datetime


otz = timezone(getattr(settings, 'OFFICIAL_TIMEZONE', 'EET'))
utc = timezone('UTC')


def strip_timezone(dt):
    if dt.tzinfo is None:
        return dt
    return (dt - dt.utcoffset()).replace(tzinfo=None)


def get_today_start():
    start = datetime.now(otz)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    return strip_timezone(start)


def get_today_end():
    end = datetime.now(otz)
    end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
    return strip_timezone(end)


def urljoin(*args):
    return path.join(args[0], *map(lambda x: x.lstrip('/'), args[1:]))


def safe_path_join(base, path, sep=path.sep):
    safe_path = sep.join(x for x in path.split(sep) if x and x != '..')
    return base.rstrip(sep) + sep + safe_path
