import logging
logger = logging.getLogger(__name__)

from os import path
try:
    from django.conf import settings
except Exception as e:
    logger.error(e)

from pytz import timezone
from datetime import datetime


ATHENS = 'Europe/Athens'

try:
    OFFICIAL_TIMEZONE = getattr(settings, 'OFFICIAL_TIMEZONE', ATHENS)
except Exception as e:
    logger.error(e)
    OFFICIAL_TIMEZONE = ATHENS


otz = timezone(OFFICIAL_TIMEZONE)
utc = timezone('UTC')


def strip_timezone(dt):
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(utc).replace(tzinfo=None)


def move_to_timezone(dt, tzinfo):
    if dt is None:
        return dt
    if dt.tzinfo is None:
        dt = utc.localize(dt)
    return dt.astimezone(tzinfo)


def at_day_start(dt, tzinfo):
    dt = move_to_timezone(dt, tzinfo)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    dt = strip_timezone(dt)
    return dt


def at_day_end(dt, tzinfo):
    dt = move_to_timezone(dt, tzinfo)
    dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    dt = strip_timezone(dt)
    return dt


def get_today_start():
    return at_day_start(datetime.utcnow(), otz)


def get_today_end():
    return at_day_end(datetime.utcnow(), otz)


def urljoin(*args):
    return path.join(args[0], *map(lambda x: x.lstrip('/'), args[1:]))


def safe_path_join(base, path, sep=path.sep):
    safe_path = sep.join(x for x in path.split(sep) if x and x != '..')
    return base.rstrip(sep) + sep + safe_path

def escape(payload):
    if (payload and isinstance(payload, basestring) and
       payload[0] in ('@', '+', '-', '=', '|', '%')):
        payload = payload.replace("|", "\|")
        payload = "'" + payload
    return payload

def write_row(sheet, datarow, row):
    col = 0
    for d in datarow:
        sheet.write(row, col, escape(d))
        col += 1
