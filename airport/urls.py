from django.urls import path, include
from rest_framework import routers

from .views import CountryViewSet, CityViewSet, AirportViewSet, RouteViewSet

router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
