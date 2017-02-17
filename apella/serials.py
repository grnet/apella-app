from django.db.models import Model, CharField, BigIntegerField
from django.conf import settings
from django.db import transaction


class Serials(Model):

    id = CharField(max_length=255, primary_key=True)
    value = BigIntegerField(default=0)

    serials = {}

    def get_serial(self, serial_name):
        new_serial, max_serial = self.serials.get(serial_name, (None, None))
        if new_serial is None or new_serial >= max_serial:
            increment = getattr(settings, 'SERIAL_ALLOCATION_INCREMENT', 1000)
            new_serial, max_serial = \
                    self.allocate_serial(serial_name, increment)

        self.serials[serial_name] = (new_serial + 1, max_serial)
        return new_serial

    def allocate_serial(self, serial_name, increment):
        autocommit = transaction.get_autocommit()
        transaction.set_autocommit(False)

        serialob = self.objects.select_for_update().get(serial_name)
        new_serial = serialob.value
        max_serial = new_serial + increment
        serialob.value = max_serial
        serialob.save()
        return new_serial
