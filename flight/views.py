from django.db.models import F, Count, Case, When, Value
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import Crew, Flight, Order
from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .serializers import (
    CrewSerializer,
    FlightSerializer,
    FlightListSerializer,
    OrderSerializer,
    OrderListSerializer,
    FlightDetailSerializer,
    OrderDetailSerializer,
)


class CrewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.select_related(
            "route__source__city__country",
            "airplane",
            "route__destination__city__country",
        )
        .prefetch_related("crew_members")
        .annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row") - Count("ticket")
            )
        )
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user).prefetch_related(
            "tickets__meal", "tickets__flight__route__source__city__country", "tickets"
        )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
