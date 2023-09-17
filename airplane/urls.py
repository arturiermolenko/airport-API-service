from django.urls import path, include
from rest_framework import routers

from .views import AirplaneTypeViewSet, AirplaneViewSet, AirlineViewSet

router = routers.DefaultRouter()
router.register("airlines", AirlineViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "airplane"
