from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import ProfessorRank, MultiLangFields


class Command(ApellaCommand):
    help = 'Create a professor rank'
    args = '<rank el> <rank en>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        rank_el, rank_en = args[:2]

        rank = MultiLangFields.objects.create(el=rank_el, en=rank_en)
        professor_rank = ProfessorRank.objects.create(rank=rank)

        self.stdout.write("Created rank %s" % professor_rank.rank.en)
