from django.db.models import Model, CharField, BigIntegerField
from django.conf import settings
from django.db import transaction


class Serials(Model):

    id = CharField(max_length=255, primary_key=True)
    value = BigIntegerField(default=0)

    serials = {}

    @classmethod
    def get_serial(cls, serial_name, nr=1):
        if nr <= 0:
            raise ValueError("Cannot get %s <= 0 serials" % nr)

        new_serial, max_serial = cls.serials.get(serial_name, (None, None))
        if new_serial is None or new_serial + nr >= max_serial:
            increment = getattr(settings, 'SERIAL_ALLOCATION_INCREMENT', 1000)
            increment += nr
            new_serial, max_serial = \
                    cls.allocate_serial(serial_name, increment)

        cls.serials[serial_name] = (new_serial + nr, max_serial)
        return new_serial

    @classmethod
    def allocate_serial(cls, serial_name, increment):
        # This must be run outside atomic blocks. If ATOMIC_REQUESTS is
        # enabled, you must run it in a middleware. Middleware run before
        # ATOMIC_REQUESTS takes effect.

        if increment <= 0:
            raise ValueError("Cannot allocate %s <= 0 serials" % increment)

        connection = transaction.get_connection()
        connection.validate_no_atomic_block()

        with transaction.atomic():
            serialob, created = cls.objects.select_for_update().\
                                get_or_create(id=serial_name)
            new_serial = serialob.value
            max_serial = new_serial + increment
            serialob.value = max_serial
            serialob.save()
        return new_serial, max_serial
