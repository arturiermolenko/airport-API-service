from django.contrib import admin

from airplane.models import AirplaneType, Airplane

admin.site.register(AirplaneType)
admin.site.register(Airplane)