from django.test import TestCase, Client
from rental_reservation.models import Rental, Reservation
from django.urls import reverse
from datetime import date
from rental_reservation import views


class ReservationsViewsTest(TestCase):
    @staticmethod
    def create_rentals(rental_names):
        return [Rental.objects.create(r) for r in rental_names]


    @staticmethod
    def create_reservation(reservations):
        for rev in reservations:
            rev.save()

    def test_no_reservations(self):
        response = self.client.get(reverse('reservation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_table'], [])

    def test_valid_reservations(self):
        rentals = self.create_rentals(rental_names=['Test Lodge', 'Test Motel', 'Test Apartments'])
        revs = [Reservation(checkin=date(year=2022, month=1, day=1),
                            checkout=date(year=2022, month=1, day=13), rental_id=rentals[0]),
                Reservation(checkin=date(year=2022, month=1, day=20),
                            checkout=date(year=2022, month=2, day=10), rental_id=rentals[0]),
                Reservation(checkin=date(year=2022, month=2, day=20),
                            checkout=date(year=2022, month=3, day=10), rental_id=rentals[0]),
                Reservation(checkin=date(year=2022, month=1, day=2),
                            checkout=date(year=2022, month=1, day=20), rental_id=rentals[1]),
                Reservation(checkin=date(year=2022, month=1, day=20),
                            checkout=date(year=2022, month=2, day=11), rental_id=rentals[1])
                ]
        self.create_reservations(revs)
        expected_query_set = [{'Rental_name': rev.get_rental_name(), 'ID': rev.id,
                               'Checkin': rev.checkin.strftime('%Y-%m-%d'), 'Checkout': rev.checkout.strftime('%Y-%m-%d'),
                               "Last_reservation": rev.previous_reservation} for rev in revs]

        response = self.client.get(reverse('reservation_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['reservation_table'], expected_query_set)
