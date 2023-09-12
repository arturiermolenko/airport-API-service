from random import choices
from string import ascii_uppercase, ascii_lowercase

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Country, City, Airport, Route
from airport.serializers import AirportSerializer, RouteListSerializer, CityListSerializer, \
    AirportListSerializer

CITIES_URL = reverse("airport:city-list")
AIRPORTS_URL = reverse("airport:airport-list")
ROUTES_URL = reverse("airport:route-list")


def sample_city():
    suffix = ("".join(choices(ascii_lowercase, k=5)))
    country = Country.objects.create(name=f"test_country_{suffix}")
    return City.objects.create(name=f"test_city_{suffix}", country=country)


def sample_airport(**params):
    suffix = ("".join(choices(ascii_lowercase, k=5)))
    country = Country.objects.create(name=f"test_country_{suffix}")
    city = City.objects.create(name=f"test_city_{suffix}", country=country)
    airport_code = ("".join(choices(ascii_uppercase, k=3)))

    defaults = {
        "name": f"test_airport_{suffix}",
        "airport_code": airport_code,
        "city": city
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route():
    source = sample_airport()
    destination = sample_airport()
    distance = 1000

    return Route.objects.create(
        source=source,
        destination=destination,
        distance=distance
    )


def get_detail_url(route_id):
    return reverse("airport:route-detail", args=[route_id])


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_city_auth_required(self):
        response = self.client.get(CITIES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_airport_auth_required(self):
        response = self.client.get(AIRPORTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_route_auth_required(self):
        response = self.client.get(ROUTES_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_cities(self):
        sample_city()
        sample_city()
        sample_city()

        response = self.client.get(CITIES_URL)

        cities = City.objects.order_by("id")
        serializer = CityListSerializer(cities, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_cities_by_country(self):
        city_1 = sample_city()
        city_2 = sample_city()
        country = Country.objects.create(name="Not match")
        city_3 = City.objects.create(name="test_city", country=country)

        response = self.client.get(CITIES_URL, {"country": "country"})

        serializer_1 = CityListSerializer(city_1)
        serializer_2 = CityListSerializer(city_2)
        serializer_3 = CityListSerializer(city_3)

        self.assertIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_3.data, response.data)

    def test_create_city_forbidden(self):
        country = Country.objects.create(name="test_country")
        data = {
            "name": "test_city",
            "country": country
        }
        response = self.client.post(CITIES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_airports(self):
        sample_airport()
        sample_airport()
        sample_airport()

        response = self.client.get(AIRPORTS_URL)

        airports = Airport.objects.order_by("id")
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_airports_by_country(self):
        airport_1 = sample_airport()
        airport_2 = sample_airport()
        country = Country.objects.create(name="Not match")
        city = City.objects.create(name="Not match", country=country)
        airport_3 = Airport.objects.create(
            name="Not match",
            airport_code="TTT",
            city=city
        )

        response = self.client.get(AIRPORTS_URL, {"city": "city"})

        serializer_1 = AirportListSerializer(airport_1)
        serializer_2 = AirportListSerializer(airport_2)
        serializer_3 = AirportListSerializer(airport_3)

        self.assertIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_3.data, response.data)

    def test_create_airport_forbidden(self):
        city = sample_city()

        data = {
            "name": "test_city",
            "airport_code": "AAA",
            "city": city
        }
        response = self.client.post(AIRPORTS_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_routes(self):
        sample_route()
        sample_route()
        sample_route()

        response = self.client.get(ROUTES_URL)

        routes = Route.objects.order_by("id")
        serializer = RouteListSerializer(routes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_routes_by_airport(self):
        route_1 = sample_route()
        route_2 = sample_route()
        city_1 = sample_city()
        city_2 = sample_city()
        airport_1 = Airport.objects.create(
            name="not_match_1",
            airport_code="TTT",
            city=city_1
        )
        airport_2 = Airport.objects.create(
            name="not_match_2",
            airport_code="TNT",
            city=city_2
        )
        route_3 = Route.objects.create(
            source=airport_1,
            destination=airport_2,
            distance=500
        )

        response = self.client.get(ROUTES_URL, {"airport": "airport"})

        serializer_1 = RouteListSerializer(route_1)
        serializer_2 = RouteListSerializer(route_2)
        serializer_3 = RouteListSerializer(route_3)

        self.assertIn(serializer_1.data, response.data)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_3.data, response.data)

    def test_create_route_forbidden(self):
        source = sample_airport()
        destination = sample_airport()

        data = {
            "source": source,
            "destination": destination,
            "distance": 400
        }
        response = self.client.post(ROUTES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_city(self):
        country = Country.objects.create(name="test_country_new")
        data = {
            "name": "test_city",
            "country": country.id
        }
        response = self.client.post(CITIES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_airport(self):
        city = sample_city()
        data = {
            "name": "test_airport",
            "airport_code": "ATE",
            "city": city.id
        }
        response = self.client.post(AIRPORTS_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_route(self):
        airport_1 = sample_airport()
        airport_2 = sample_airport()

        data = {
            "source": airport_1.id,
            "destination": airport_2.id,
            "distance": 500
        }
        response = self.client.post(ROUTES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_route_not_allowed(self):
        airport_1 = sample_airport()
        airport_2 = sample_airport()
        route = sample_route()
        data = {
            "source": airport_1.id,
            "destination": airport_2.id,
            "distance": 500
        }

        url = get_detail_url(route.id)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_movie_not_allowed(self):
        route = sample_route()
        url = get_detail_url(route.id)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
