from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import ProfessorRank, MultiLangFields


class Command(ApellaCommand):
    help = 'Create a professor rank'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rank-el',
            dest='rank_el',
            help='Professor rank name in Greek',
            required=True,
        )

        parser.add_argument(
            '--rank-en',
            dest='rank_en',
            help='Professor rank name in English',
            required=True,
        )

    def handle(self, *args, **options):
        rank_el = options['rank_el']
        rank_en = options['rank_en']

        if ProfessorRank.objects.filter(rank__el=rank_el):
            self.stdout.write("Rank exists %s" % rank_el)
            return

        rank = MultiLangFields.objects.create(el=rank_el, en=rank_en)
        professor_rank = ProfessorRank.objects.create(rank=rank)

        self.stdout.write("Created rank %s" % professor_rank.rank.en)
