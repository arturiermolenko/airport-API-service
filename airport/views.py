from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from flight.permissions import IsAdminOrIfAuthenticatedReadOnly
from .models import (
    Country,
    City,
    Airport,
    Route
)
from .serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    RouteDetailSerializer,
    AirportCreateSerializer,
    RouteListSerializer
)


class CountryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class CityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        country = self.request.query_params.get("country")
        queryset = self.queryset

        if country:
            queryset = queryset.filter(
                country__name__icontains=country
            )

        return queryset


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.select_related("city")
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        city = self.request.query_params.get("city")
        queryset = self.queryset

        if city:
            queryset = queryset.filter(
                city__name__icontains=city
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return AirportCreateSerializer

        return AirportSerializer


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Route.objects.select_related(
        "destination__city",
        "source__city",
    )
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer
