import datetime
import random
from random import choices
from string import ascii_lowercase

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airplane.tests.test_airplane_api import sample_airplane
from airport.tests.test_airport_api import sample_route
from flight.models import Crew, Flight, Meal, Ticket, Order
from flight.serializers import CrewSerializer, FlightListSerializer, OrderListSerializer

CREW_URL = reverse("flight:crew-members-list")
FLIGHT_URL = reverse("flight:flight-list")
ORDER_URL = reverse("flight:order-list")


def get_detail_order_url(route_id):
    return reverse("flight:order-detail", args=[route_id])


def get_detail_flight_url(flight_id):
    return reverse("flight:flight-detail", args=[flight_id])


def sample_crew_member():
    suffix = "".join(choices(ascii_lowercase, k=5))
    return Crew.objects.create(
        first_name=f"test_first_name_{suffix}",
        last_name=f"test_last_name_{suffix}",
        position=f"test_position_{suffix}",
    )


def sample_departure_time():
    date_str = "2023-02-28 14:30:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(date_str, date_format) + datetime.timedelta(
        hours=random.randint(1, 100)
    )


def sample_flight():
    departure_time = sample_departure_time()
    route = sample_route()
    airplane = sample_airplane()
    flight = Flight.objects.create(
        route=route,
        airplane=airplane,
        departure_time=departure_time,
        arrival_time=(departure_time + datetime.timedelta(hours=2)),
    )
    return flight


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_crew_auth_required(self):
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_flight_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew_member()
        sample_crew_member()
        sample_crew_member()

        response = self.client.get(CREW_URL)

        crew_members = Crew.objects.order_by("position")
        serializer = CrewSerializer(crew_members, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_crew_member_forbidden(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "position": "test_position",
        }
        response = self.client.post(CREW_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_flight(self):
        sample_flight()
        sample_flight()
        sample_flight()

        response = self.client.get(FLIGHT_URL)
        data = response.data
        for flight in data:
            del flight["tickets_available"]

        flights = Flight.objects.order_by("id")
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, serializer.data)

    def test_create_flight_forbidden(self):
        route = sample_route()
        airplane = sample_airplane()
        departure_time = sample_departure_time()
        data = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": (departure_time + datetime.timedelta(hours=2)),
        }
        response = self.client.post(FLIGHT_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list(self):
        flight = sample_flight()
        meal = Meal.objects.create()

        order_1 = Order.objects.create(user=self.user)
        order_2 = Order.objects.create(user=self.user)
        order_3 = Order.objects.create(user=self.user)

        Ticket.objects.create(
            row=1,
            seat=1,
            flight=flight,
            order=order_1,
            meal=meal,
            ticket_class="ECONOMY",
        ),
        Ticket.objects.create(
            row=1,
            seat=2,
            flight=flight,
            order=order_2,
            meal=meal,
            ticket_class="BUSINESS",
        )
        Ticket.objects.create(
            row=1,
            seat=3,
            flight=flight,
            order=order_3,
            meal=meal,
            ticket_class="ECONOMY",
        )

        response = self.client.get(ORDER_URL)

        orders = Order.objects.order_by("-created_at")
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_order_list_of_different_user_cannot_be_received(self):
        flight = sample_flight()
        meal = Meal.objects.create()
        order = Order.objects.create(user=self.user)
        Ticket.objects.create(
            row=1, seat=1, flight=flight, order=order, meal=meal, ticket_class="ECONOMY"
        )

        self.client.logout()
        self.new_client = APIClient()
        self.new_user = get_user_model().objects.create_user(
            "new_test@test.com",
            "testpass",
        )
        self.new_client.force_authenticate(self.new_user)

        response = self.new_client.get(ORDER_URL)

        self.assertNotIn(order, response.data)
        self.assertNotIn(order.tickets, response.data)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_crew_member(self):
        data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "position": "test_position",
        }
        response = self.client.post(CREW_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        departure_time = sample_departure_time()
        data = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": (departure_time + datetime.timedelta(hours=2)),
        }
        response = self.client.post(FLIGHT_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_flight(self):
        flight = sample_flight()
        departure_time = sample_departure_time()
        data = {
            "departure_time": departure_time,
        }

        url = get_detail_flight_url(flight_id=flight.id)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        flight = sample_flight()
        departure_time = sample_departure_time()
        data = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure_time,
            "arrival_time": (departure_time + datetime.timedelta(hours=2)),
        }
        url = get_detail_flight_url(flight_id=flight.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_flight(self):
        flight = sample_flight()

        url = get_detail_flight_url(flight_id=flight.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_order_not_allowed(self):
        flight = sample_flight()
        meal = Meal.objects.create()
        order = Order.objects.create(user=self.user)
        created_at = sample_departure_time()
        Ticket.objects.create(
            row=1, seat=1, flight=flight, order=order, meal=meal, ticket_class="ECONOMY"
        )
        data = {"created_at": created_at, "user": 1}

        url = get_detail_order_url(order.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_route_not_allowed(self):
        flight = sample_flight()
        meal = Meal.objects.create()
        order = Order.objects.create(user=self.user)
        Ticket.objects.create(
            row=1, seat=1, flight=flight, order=order, meal=meal, ticket_class="ECONOMY"
        )

        url = get_detail_order_url(order.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
