from django.db.utils import IntegrityError
from django.test import TestCase

from airport.models import Country, City, Airport, Route


class AirportModelsTests(TestCase):
    def setUp(self):
        country_1 = Country.objects.create(name="test_country_1")
        country_2 = Country.objects.create(name="test_country_2")
        city_1 = City.objects.create(name="test_city_1", country=country_1)
        city_2 = City.objects.create(name="test_city_2", country=country_2)
        airport_1 = Airport.objects.create(
            name="test_airport_1", city=city_1, airport_code="TES"
        )
        airport_2 = Airport.objects.create(
            name="test_airport_2", city=city_2, airport_code="SET"
        )
        Route.objects.create(source=airport_1, destination=airport_2, distance=1000)

    def test_country_str(self):
        country = Country.objects.first()

        self.assertEqual(str(country), country.name)

    def test_city_str(self):
        city = City.objects.first()

        self.assertEqual(str(city), f"{city.country.name}: {city.name}")

    def test_airport_str(self):
        airport = Airport.objects.first()

        self.assertEqual(str(airport), airport.name)

    def test_route_str(self):
        route = Route.objects.first()

        self.assertEqual(str(route), f"{route.source} - {route.destination}")

    def test_route_unique_together(self):
        airport_1 = Airport.objects.first()
        airport_2 = Airport.objects.get(id=airport_1.id + 1)

        with self.assertRaises(IntegrityError):
            Route.objects.create(source=airport_1, destination=airport_2, distance=1000)

    def test_route_code(self):
        route = Route.objects.first()

        self.assertEqual(
            route.code,
            (
                f"{route.source.city}: {route.source.airport_code} - "
                f"{route.destination.city}: {route.destination.airport_code}"
            ),
        )
