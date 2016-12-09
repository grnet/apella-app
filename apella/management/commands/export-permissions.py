import json

from collections import defaultdict
from apella.permissions.permission_rules import PERMISSION_RULES
from apella.management.utils import ApellaCommand


def to_dict(data, args):
    if len(args) == 1:
        return args[0]

    key = args.pop(0)
    for k in key.split(","):
        k = k.strip()
        data[k] = data[k] if k in data else {}
        partial = {
            k: to_dict(data[k], args)
        }
        data.update(partial)
    return data

class Command(ApellaCommand):
    help = 'Export permissions rules to json format'
    args = ''

    def handle(self, *args, **options):
        PERMISSIONS = defaultdict(lambda: dict)
        for rule in PERMISSION_RULES:
            to_dict(PERMISSIONS, list(rule))
        print json.dumps(PERMISSIONS, indent=2)
