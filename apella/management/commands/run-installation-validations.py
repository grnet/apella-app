from django.core.management.base import CommandError
from django.conf import settings
from apella.installation_validations import validate_installation
from apella.management.utils import ApellaCommand


class Command(ApellaCommand):
    help = 'Run apella.installation_validations.validate_installation()'

    def handle(self, *args, **options):
        validate_installation()
