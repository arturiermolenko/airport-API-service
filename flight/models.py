from django.core.exceptions import ValidationError
from django.db import models

from airplane.models import Airplane
from airport.models import Route
from django.conf import settings


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    class Meta:
        verbose_name = "crew_member"
        verbose_name_plural = "crew_members"
        ordering = ["position"]

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Meal(models.Model):
    STANDARD = "STANDARD"
    VEGETARIAN = "VEGETARIAN"
    NO_MEAL = "NO_MEAL"
    MEAL_CHOICES = [
        (STANDARD, "Standard"),
        (VEGETARIAN, "Vegetarian"),
        (NO_MEAL, "No meal"),
    ]

    meal = models.CharField(max_length=10, choices=MEAL_CHOICES, default=STANDARD)

    def __str__(self):
        return self.meal


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    crew_members = models.ManyToManyField(Crew, blank=False, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["departure_time"]

    def __str__(self):
        return self.route.code


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    ECONOMY = "ECONOMY"
    BUSINESS = "BUSINESS"
    CLASS_CHOICES = [(ECONOMY, "Economy"), (BUSINESS, "Business")]

    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    ticket_class = models.CharField(
        max_length=8, choices=CLASS_CHOICES, default=ECONOMY
    )

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row, self.seat, self.flight.airplane, ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{self.flight} "
            f"(row: {self.row}, "
            f"seat: {self.seat}, "
            f"meal: {self.meal}"
        )
