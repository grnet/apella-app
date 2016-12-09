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
        make_option('--state',
                    dest='state',
                    help='Set state for the position. Available states are \
                        "cancelled", "electing", "failed"'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        position_id = args[0]
        elected = options['elected']
        electors = options['electors']
        committee = options['committee']
        state = options['state']

        try:
            position = Position.objects.get(id=position_id)
        except (Position.DoesNotExist, ValueError):
            raise CommandError("Invalid position ID")

        if state:
            try:
                ["cancelled", "electing", "failed", "revoked"].index(state)
                if state == "cancelled":
                    if position.state != "posted":
                        self.stdout.write(
                            "Position %s cannot be cancelled. Only positions \
                            in state posted can be cancelled" % position.id)
                    elif position.starts_at.date() < datetime.today().date():
                        self.stdout.write(
                            "Position %s cannot be cancelled. Open positions \
                            cannot be cancelled" % position.id)
                    else:
                        position.state = 'cancelled'
                        position.save()
                        self.stdout.write(
                            "Position %s has been cancelled" % position.id)

                if state == "failed":
                    if position.state != "electing":
                        self.stdout.write(
                            "Position %s cannot be set to failed. Only \
                            positions in state electing can be set to failed\
                            " % position.id)
                    else:
                        position.state = 'failed'
                        position.save()
                        self.stdout.write(
                            "Position %s has been set to failed" % position.id)

                if state == "revoked":
                    if position.state != "electing":
                        self.stdout.write(
                            "Position %s cannot be revoked. Only positions in \
                            state electing can be set to failed" % position.id)
                    else:
                        position.state = 'revoked'
                        position.save()
                        self.stdout.write(
                            "Position %s has been set to revoked" % position.id)

                if state == "electing":
                    if position.state != "posted":
                        self.stdout.write(
                            "Position %s cannot be set to electing. Only \
                             posted positions cannot be set to electing \
                             " % position.id)

                    elif position.ends_at.date() > datetime.today().date():
                        self.stdout.write(
                            "Position %s cannot be set to electing as it is \
                            still accepting candidacies" % position.id)

                    else:
                        position.state = 'electing'
                        position.save()
                        self.stdout.write(
                            "Position %s has been set to electing" % position.id)
            except:
                raise CommandError("State: %s is an invalid state" % state)

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
