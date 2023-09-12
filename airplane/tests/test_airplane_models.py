from django.test import TestCase

from airplane.models import Airline, AirplaneType, Airplane


class AirplaneModelTests(TestCase):
    def test_airline_str(self):
        airline = Airline.objects.create(name="test_airline")

        self.assertEqual(str(airline), airline.name)

    def test_airplane_type_str(self):
        airplane_type = AirplaneType.objects.create(name="test_airline_type")

        self.assertEqual(str(airplane_type), airplane_type.name)

    def test_airplane_str(self):
        airplane_type = AirplaneType.objects.create(name="test_type")
        airline = Airline.objects.create(name="test_airline")

        defaults = {
            "name": "test_name",
            "rows": 30,
            "seats_in_row": 8,
            "airplane_type": airplane_type,
            "airline": airline
        }

        airplane = Airplane.objects.create(**defaults)

        self.assertEqual(
            str(airplane),
            f"{airplane.name}, capacity: {airplane.capacity}"
        )

    def test_airplane_capacity(self):
        airplane_type = AirplaneType.objects.create(name="test_type")
        airline = Airline.objects.create(name="test_airline")

        defaults = {
            "name": "test_name",
            "rows": 30,
            "seats_in_row": 8,
            "airplane_type": airplane_type,
            "airline": airline
        }

        airplane = Airplane.objects.create(**defaults)
        capacity = airplane.rows * airplane.seats_in_row

        self.assertEqual(
            capacity,
            airplane.capacity
        )
