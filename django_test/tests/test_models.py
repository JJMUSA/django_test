from django.test import TestCase
from rental_reservation.models import Rental, Reservation, InvalidRentalNameException, InvalidReservationDateException
from datetime import datetime,date


class RentalTest(TestCase):
    def test_valid_rental_name(self):
        rental = Rental.objects.create(name='Test Lodge')
        self.assertEqual(rental.name, 'Test Lodge')

    def test_invalid_rental_name(self):
        self.assertRaises(InvalidRentalNameException, Rental.objects.create, name='123')


class ReservationTest(TestCase):
    def test_valid_reservation(self):
        rental = Rental.objects.create(name="Test Motel")
        checkin_date = datetime(year=2022, month=1, day=1)
        checkout_date = datetime(year=2022, month=1, day=13)
        reservation = Reservation(checkin=checkin_date, checkout=checkout_date, rental_id=rental)
        self.assertEqual(reservation.rental_id, rental)
        self.assertEqual(reservation.checkin, checkin_date)
        self.assertEqual(reservation.checkout, checkout_date)

    def test_previous_reservation(self):
        rental = Rental.objects.create(name="Test Motel")

        checkin1_date = date(year=2022, month=1, day=1)
        checkout1_date = date(year=2022, month=1, day=13)
        reservation1 = Reservation.objects.create(checkin=checkin1_date, checkout=checkout1_date, rental_id=rental)

        checkin2_date = date(year=2022, month=1, day=20)
        checkout2_date = date(year=2022, month=2, day=10)
        reservation2 = Reservation.objects.create(checkin=checkin2_date, checkout=checkout2_date, rental_id=rental)

        checkin3_date = date(year=2022,month=2, day=20)
        checkout3_date = date(year=2022, month=3, day=10)
        reservation3 = Reservation.objects.create(checkin=checkin3_date, checkout=checkout3_date, rental_id=rental)

        self.assertEqual(reservation3.previous_reservation, reservation2.id)
        self.assertGreater(reservation3.checkin, Reservation.objects.get(pk=reservation3.previous_reservation).checkin)

    def test_reservation_checkin_before_last_checkout(self):
        rental = Rental.objects.create(name="Test Lodge")

        checkin1_date = date(year=2022, month=1, day=2)
        checkout1_date = date(year=2022, month=1, day=20)
        reservation1 = Reservation.objects.create(checkin=checkin1_date, checkout=checkout1_date, rental_id=rental)

        checkin2_date = date(2022, 1, 10)
        checkout2_date = date(2022, 1, 30)
        self.assertRaises(InvalidReservationDateException, Reservation.objects.create, checkin=checkin2_date,
                          checkout=checkout2_date, rental_id=rental)

    def test_checkout_before_checkin(self):
        rental = Rental.objects.create(name="Test Lodge")
        checkin_date = date(year=2022,month=2, day=20)
        checkout_date = date(year=2022, month=2, day=10)

        self.assertRaises(InvalidReservationDateException, Reservation.objects.create, checkin=checkin_date,
                          checkout=checkout_date, rental_id=rental)




