
from .models import Rental, Reservation
from django.shortcuts import render
# Create your views here.


def get_reservations(request):
    all_reservation = Reservation.objects.all()
    table = [{'Rental_name': rev.rental_id.name, 'ID': rev.id,
              'Checkin': rev.checkin.strftime('%Y-%m-%d'), 'Checkout': rev.checkout.strftime('%Y-%m-%d'),
              "Last_reservation": rev.previous_reservation} for rev in all_reservation]
    context = {'reservation_table': table}
    return render(request, 'reservation_list.html', context)
