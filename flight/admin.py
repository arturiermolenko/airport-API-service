from django.contrib import admin

from flight.models import Crew, Meal, Flight, Order, Ticket

admin.site.register(Crew)
admin.site.register(Meal)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
