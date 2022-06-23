
from .models import Rental, Reservation
from django.shortcuts import render
from django.db.models import Subquery, OuterRef, F
from django.db.models.functions import Coalesce
# Create your views here.


def get_reservations(request):
    previous_reservation_query = Reservation.objects.filter(checkin__lt=OuterRef('checkin'),
                                                            rental_id=OuterRef('rental_id')).order_by('checkin')

    all_reservation = Reservation.objects.annotate(rental_name=F('rental_id__name'),
                                                   previous_rev=Subquery(previous_reservation_query.values('id').reverse()[:1]))

    table = [{'Rental_name': rev.rental_name, 'ID': rev.id,
              'Checkin': rev.checkin.strftime('%Y-%m-%d'), 'Checkout': rev.checkout.strftime('%Y-%m-%d'),
              "Last_reservation": rev.previous_rev} for rev in all_reservation]
    context = {'reservation_table': table}
    return render(request, 'reservation_list.html', context)
