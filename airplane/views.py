from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from flight.permissions import IsAdminOrIfAuthenticatedReadOnly
from .models import AirplaneType, Airplane, Airline
from .serializers import (
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirlineSerializer,
)


class AirlineViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneTypeViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AirplaneViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Airplane.objects.select_related("airplane_type", "airline")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        return AirplaneSerializer
