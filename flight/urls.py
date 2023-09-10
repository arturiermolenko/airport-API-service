from django.urls import path, include
from rest_framework import routers

from .views import (
    CrewViewSet,
    FlightViewSet,
    OrderViewSet
)

router = routers.DefaultRouter()
router.register("crew-members", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "flight"
