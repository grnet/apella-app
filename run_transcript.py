#! /usr/bin/env python
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apella_app.settings")

import json
import django
from collections import OrderedDict

django.setup()

from django.core import management
from apella.management.commands import *

reload(sys)
sys.setdefaultencoding('utf8')


def run_command(command, input=None):
    args = []
    options = []
    if input:
        for key in input:
            if key.startswith('arg'):
                args.append(str(input[key]))
            else:
                options.append((key, str(input[key])))
    management.call_command(command, *args, **dict(options))

with open(sys.argv[1]) as jdata:
    data = json.load(jdata, object_pairs_hook=OrderedDict)

for a in data["actions"]:
    try:
        run_command(command=str(a["action"]), input=a["input"])
    except KeyError:
        run_command(command=str(a["action"]))
