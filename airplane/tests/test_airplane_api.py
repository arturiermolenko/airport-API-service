from random import randint

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airplane.models import AirplaneType, Airline, Airplane
from airplane.serializers import AirplaneSerializer, AirplaneListSerializer

AIRPLANE_URL = reverse("airplane:airplane-list")


def sample_airplane(**params):
    airplane_type = AirplaneType.objects.create(name="test_type")
    airline = Airline.objects.create(name="test_airline")

    defaults = {
        "name": f"test_name{randint(1, 100000)}",
        "rows": 30,
        "seats_in_row": 8,
        "airplane_type": airplane_type,
        "airline": airline
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        sample_airplane()

        response = self.client.get(AIRPLANE_URL)

        airplanes = Airplane.objects.order_by("id")
        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airplanes_by_name(self):
        airplane1 = sample_airplane()
        airplane2 = sample_airplane()
        airplane3 = sample_airplane(name="Not match")

        response = self.client.get(AIRPLANE_URL, {"name": "name"})

        serializer1 = AirplaneListSerializer(airplane1)
        serializer2 = AirplaneListSerializer(airplane2)
        serializer3 = AirplaneListSerializer(airplane3)

        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)
        self.assertNotIn(serializer3.data, response.data)

    def test_create_airplane_forbidden(self):
        airplane_type = AirplaneType.objects.create(name="test_type_new")
        airline = Airline.objects.create(name="test_airline_new")

        data = {
            "name": "test_name_new",
            "rows": 30,
            "seats_in_row": 8,
            "airplane_type": airplane_type,
            "airline_name": airline
        }
        response = self.client.post(AIRPLANE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_airplane(self):
        airplane_type = AirplaneType.objects.create(name="test_new")
        airline = Airline.objects.create(name="test_new")

        data = {
            "name": "test_new",
            "rows": 30,
            "seats_in_row": 8,
            "airplane_type": airplane_type.id,
            "airline": airline.id
        }
        response = self.client.post(AIRPLANE_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
