from django.urls import path, include
from rest_framework import routers

from .views import (
    CrewViewSet,
    FlightViewSet,
    TicketViewSet,
    OrderViewSet
)

router = routers.DefaultRouter()
router.register("crew-members", CrewViewSet)
router.register("flights", FlightViewSet)
# router.register("tickets", TicketViewSet)
# router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "flight"
