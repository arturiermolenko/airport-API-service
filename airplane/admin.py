from django.contrib import admin

from airplane.models import AirplaneType, Airplane, Airline

admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airline)
