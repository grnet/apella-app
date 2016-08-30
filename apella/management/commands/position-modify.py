from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position
from apella.management.utils import get_user


class Command(BaseCommand):
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
        )


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        position_id = args[0]
        elected = options['elected']
        electors = options['electors']
        committee = options['committee']

        try:
            position = Position.objects.get(id=position_id)
        except (Position.DoesNotExist, ValueError):
            raise CommandError("Invalid position ID")

        if elected:
            try:
                elected = get_user(elected)
                position.elected = elected
                position.state = '4'
                position.save()
                self.stdout.write("%s has been elected for position %s" %
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
                        u = get_user(e)
                        position.electors.add(u)
                        position.state = '3'
                        position.save()
                        self.stdout.write(
                                "%s is an elector for position %s" %
                                (u.username, position.id))

                    except ApellaUser.DoesNotExist:
                        raise CommandError("Invalid elector ID %s" % e)
                    except:
                        raise CommandError("Operation failed")

            except TypeError:
                    print 'Electors should be comma separated user ids'


        if committee:
            try:
                committee_ids = committee.split(',')
                for c in committee_ids:
                    try:
                        u = get_user(c)
                        position.committee.add(u)
                        position.state = '3'
                        position.save()
                        self.stdout.write(
                                "%s is in committee for position %s" %
                                (u.username, position.id))

                    except ApellaUser.DoesNotExist:
                        raise CommandError("Invalid elector ID %s" % c)
                    except:
                        raise CommandError("Operation failed")

            except TypeError:
                    print 'Committee should be comma separated user ids'
