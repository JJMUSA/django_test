from django.db import models
from django.utils import timezone
from datetime import date


class Rental(models.Model):
    name = models.CharField(null=False, max_length=30)

    def save(self, *args, **kwargs):
        if any([char.isalpha() for char in self.name]):
            super(Rental, self).save(*args, **kwargs)
        else:
            raise InvalidRentalNameException()


class Reservation(models.Model):
    checkin = models.DateField(blank=False, null=False)
    checkout = models.DateField(blank=False, null=False)
    rental_id = models.ForeignKey(to=Rental, on_delete=models.CASCADE, null=False)

    @property
    def previous_reservation(self):
        try:
            return Reservation.objects.filter(rental_id=self.rental_id, checkin__lt=self.checkin).latest("checkin").id
        except Reservation.DoesNotExist:
            return None

    def get_rental_name(self):
        return self.rental_id.name

    def save(self, *args, **kwargs):
        # checkout of the previous reservation
        previous_rev_checkout = Reservation.objects.get(pk=self.previous_reservation).checkout \
            if not (self.previous_reservation is None) else self.checkin

        # reservation checkin must be greater than or equal to last checkout and greater than reservation checkout
        if previous_rev_checkout <= self.checkin < self.checkout:
            super(Reservation, self).save(*args, **kwargs)
        else:
            raise InvalidReservationDateException


class InvalidReservationDateException(Exception):
    pass


class InvalidRentalNameException(Exception):
    pass