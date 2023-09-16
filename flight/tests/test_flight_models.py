import datetime
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from airplane.models import AirplaneType, Airline, Airplane
from airplane.tests.test_airplane_api import sample_airplane
from airport.tests.test_airport_api import sample_route
from flight.models import Crew, Flight, Meal, Order, Ticket


class FlightModelsTests(TestCase):
    def setUp(self):
        crew_member = Crew.objects.create(
            first_name="test_first_name",
            last_name="test_last_name",
            position="test_position",
        )
        route = sample_route()
        airplane = sample_airplane()
        flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time=datetime.datetime.now(),
            arrival_time=(datetime.datetime.now() + datetime.timedelta(hours=2)),
        )
        flight.save()
        flight.crew_members.add(crew_member.id)
        user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        order = Order.objects.create(user=user)
        meal = Meal.objects.create()
        Ticket.objects.create(
            row=1, seat=1, flight=flight, order=order, meal=meal, ticket_class="ECONOMY"
        )

    def test_crew_member_str(self):
        crew_member = Crew.objects.first()

        self.assertEqual(
            str(crew_member), crew_member.first_name + " " + crew_member.last_name
        )

    def test_crew_member_full_name(self):
        crew_member = Crew.objects.first()

        self.assertEqual(
            crew_member.full_name, f"{crew_member.first_name} {crew_member.last_name}"
        )

    def test_meal_str(self):
        meal = Meal.objects.create()
        self.assertEqual(str(meal), meal.meal)

    def test_flight_str(self):
        flight = Flight.objects.first()

        self.assertEqual(str(flight), flight.route.code)

    def test_order_str(self):
        order = Order.objects.first()

        self.assertEqual(str(order), str(order.created_at))

    def test_ticket_str(self):
        ticket = Ticket.objects.first()

        self.assertEqual(
            str(ticket),
            (
                f"{ticket.flight} "
                f"(row: {ticket.row}, "
                f"seat: {ticket.seat}, "
                f"meal: {ticket.meal}"
            ),
        )

    def test_ticket_unique_together(self):
        date_str = "2023-02-28 14:30:00"
        date_format = "%Y-%m-%d %H:%M:%S"
        departure_time = datetime.datetime.strptime(
            date_str, date_format
        ) + datetime.timedelta(hours=random.randint(1, 100))
        with self.assertRaises(IntegrityError):
            route = sample_route()
            airplane = sample_airplane()
            flight = Flight.objects.create(
                route=route,
                airplane=airplane,
                departure_time=departure_time,
                arrival_time=(departure_time + datetime.timedelta(hours=2)),
            )
            user = get_user_model().objects.create_user(
                "admin@admin.com", "testpass", is_staff=True
            )
            order = Order.objects.create(user=user)
            meal = Meal.objects.create()
            Ticket.objects.create(
                row=1,
                seat=1,
                flight=flight,
                order=order,
                meal=meal,
                ticket_class="ECONOMY",
            )

    def test_validate_ticket(self):
        airplane_type = AirplaneType.objects.create(name="test_type")
        airline = Airline.objects.create(name="test_airline")
        airplane = Airplane.objects.create(
            name="test_name",
            rows=30,
            seats_in_row=8,
            airplane_type=airplane_type,
            airline=airline,
        )

        with self.assertRaises(ValidationError):
            Ticket.validate_ticket(
                row=30, seat=9, airplane=airplane, error_to_raise=ValidationError
            )

        with self.assertRaises(ValidationError):
            Ticket.validate_ticket(
                row=31, seat=8, airplane=airplane, error_to_raise=ValidationError
            )
