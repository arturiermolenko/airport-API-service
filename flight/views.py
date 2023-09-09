from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Crew, Flight
from .permissions import IsAdminOrIfAuthenticatedReadOnly
from .serializers import CrewSerializer, FlightSerializer, FlightListSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class FlightViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = (
        Flight.objects.
        select_related("route", "airplane").
        prefetch_related("crew_members")
    )
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        return FlightSerializer


class TicketViewSet:
    pass


class OrderViewSet:
    pass
