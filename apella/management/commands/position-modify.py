from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position, Professor
from apella.management.utils import get_user, ApellaCommand
from datetime import datetime


class Command(ApellaCommand):
    help = 'Update a position'
    args = '<position ID>'

    option_list = BaseCommand.option_list + (
        make_option('--elected',
                    dest='elected',
                    help='Choose an elected user for the position'),
        make_option('--electors',
                    dest='electors',
                    help='Choose electors for the position'),
        make_option('--committee',
                    dest='committee',
                    help='Choose committee for the position'),
        make_option('--cancel',
                    dest='cancel',
                    help='Cancel position'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        position_id = args[0]
        elected = options['elected']
        electors = options['electors']
        committee = options['committee']
        cancel = options['cancel']

        try:
            position = Position.objects.get(id=position_id)
        except (Position.DoesNotExist, ValueError):
            raise CommandError("Invalid position ID")

        if cancel:
            if position.state != "posted":
                self.stdout.write(
                    "Only positions in state posted can be cancelled")
            elif position.starts_at.date() < datetime.today().date():
                self.stdout.write(
                    "Open positions cannot be cancelled")
            else:
                position.state = 'cancelled'
                position.save()
                self.stdout.write(
                    "Position %s has been cancelled" % position.id)

        if elected:
            try:
                elected = get_user(elected)
                position.elected = elected
                position.state = 'successful'
                position.save()
                self.stdout.write(
                    "%s has been elected for position %s" %
                    (elected.username, position.id))

            except ApellaUser.DoesNotExist:
                raise CommandError("Invalid elected ID")
            except:
                raise CommandError("Operation failed")

        if electors:
            try:
                electors_ids = electors.split(',')
                for e in electors_ids:
                    try:
                        u = Professor.objects.get(id=e)
                        position.electors.add(u)
                        position.state = 'electing'
                        position.save()
                        self.stdout.write(
                                "%s is an elector for position %s" %
                                (u.user.username, position.id))

                    except Professor.DoesNotExist:
                        raise CommandError("Invalid professor ID %s" % e)
                    except:
                        raise CommandError("Operation failed")

            except TypeError:
                    print 'Electors should be comma separated user ids'

        if committee:
            try:
                committee_ids = committee.split(',')
                for c in committee_ids:
                    try:
                        u = Professor.objects.get(id=c)
                        position.committee.add(u)
                        position.state = 'electing'
                        position.save()
                        self.stdout.write(
                                "%s is in committee for position %s" %
                                (u.user.username, position.id))

                    except Professor.DoesNotExist:
                        raise CommandError("Invalid professor ID %s" % c)
                    except:
                        raise CommandError("Operation failed")

            except TypeError:
                    print 'Committee should be comma separated user ids'
