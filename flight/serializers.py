from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airplane.serializers import AirplaneSerializer
from airport.serializers import RouteListSerializer
from .models import Crew, Flight, Ticket, Order


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "full_name", "position")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
        )


class FlightListSerializer(FlightSerializer):
    route = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="code"
    )
    airplane = serializers.StringRelatedField(
        many=False,
        read_only=True
    )
    crew_members = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew_members",
            "departure_time",
            "arrival_time",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
            "ticket_class",
            "meal"
        )

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data


class TicketListSerializer(TicketSerializer):
    flight = serializers.StringRelatedField(many=False, read_only=True)
    meal = serializers.CharField(
        source="meal.meal",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
            "ticket_class",
            "meal"
        )


class TicketDetailSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)
    meal = serializers.CharField(
        source="meal.meal",
        read_only=True
    )

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
            "ticket_class",
            "meal"
        )


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat", "ticket_class", "meal")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "taken_places",
            "departure_time",
            "arrival_time")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)
