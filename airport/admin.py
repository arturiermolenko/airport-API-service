from django.contrib import admin

from airport.models import Country, City, Airport, Route

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Route)
