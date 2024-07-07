from django.contrib import admin
from .models import Restaurant, Reservation


admin.site.register(Restaurant)
admin.site.register(Reservation)