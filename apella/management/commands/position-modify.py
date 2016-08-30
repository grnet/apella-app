from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position


class Command(BaseCommand):
    help = 'Update a position'
    args = '<position ID>'

    option_list = BaseCommand.option_list + (
        make_option('--set-elected',
                    dest='elected',
                    help='Choose an elected user for the position'),
        make_option('--set-electors',
                    dest='electors',
                    help='Choose electors for the position'),
        make_option('--set-committee',
                    dest='committee',
                    help='Choose committee for the position'),
        )


    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Please provide a position ID")
        position_id = args[0]
        elected = options['elected']
        electors = options['electors']
        committee = options['committee']

        if position_id.isdigit():
            try:
                position = Position.objects.get(id=int(position_id))
            except Position.DoesNotExist:
                raise CommandError("Invalid position ID")
        else:
            raise CommandError("Position ID must be an integer")

        if elected:
            if elected.isdigit():
                try:
                    elected = ApellaUser.objects.get(id=int(elected))
                    position.elected = elected
                    position.save()
                    self.stdout.write("%s has been elected for position %s" %
                            (elected.username, position.id))

                except ApellaUser.DoesNotExist:
                    raise CommandError("Invalid elected ID")
                except:
                    raise CommandError("Operation failed")

            else:
                raise CommandError("Elected ID must be an integer")

        if electors:
            try:
                electors_ids = electors.split(',')
                for e in electors_ids:
                    if e.isdigit():
                        try:
                            u = ApellaUser.objects.get(id=int(e))
                            position.electors.add(u)
                            position.save()
                            self.stdout.write(
                                    "%s is an elector for position %s" %
                                    (u.username, position.id))

                        except ApellaUser.DoesNotExist:
                            raise CommandError("Invalid elector ID %s" % e)
                        except:
                            raise CommandError("Operation failed")
                    else:
                        raise CommandError(
                                "Elector ID %s  must be an integer" % e)

            except TypeError:
                    print 'Electors should be comma separated user ids'


        if committee:
            try:
                committee_ids = committee.split(',')
                for c in committee_ids:
                    if c.isdigit():
                        try:
                            u = ApellaUser.objects.get(id=int(c))
                            position.committee.add(u)
                            position.save()
                            self.stdout.write(
                                    "%s is in committee for position %s" %
                                    (u.username, position.id))

                        except ApellaUser.DoesNotExist:
                            raise CommandError("Invalid elector ID %s" % c)
                        except:
                            raise CommandError("Operation failed")
                    else:
                        raise CommandError(
                                "Elector ID %s  must be an integer" % c)

            except TypeError:
                    print 'Committee should be comma separated user ids'
