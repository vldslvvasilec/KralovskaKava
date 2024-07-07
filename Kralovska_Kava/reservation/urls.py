from django.urls import path
from .views import IndexView, GetAvailableDatesView, GetAvailableTimesView, makeReservationView, reservation_success_view, reservation_error_view

urlpatterns = [
    path('', IndexView.as_view(), name='reservation'),
    path('get-available-dates/', GetAvailableDatesView.as_view(), name='get_available_dates'),
    path('get-available-times/', GetAvailableTimesView.as_view(), name='get_available_times'),
    path('make/', makeReservationView, name='make_reservation'),
    path('success/', reservation_success_view, name='reservation_success'),
    path('error/', reservation_error_view, name='reservation_error'),
]
