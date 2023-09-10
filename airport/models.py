from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "country"
        verbose_name_plural = "countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        ordering = ["country"]

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    airport_code = models.CharField(max_length=3, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        ordering = ["city"]

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="source"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="destination"
    )
    distance = models.IntegerField()

    class Meta:
        unique_together = ("source", "destination")

    def __str__(self):
        return f"{self.source} - {self.destination}"

    @property
    @extend_schema_field(OpenApiTypes.STR)
    def code(self):
        return (f"{self.source.city}: {self.source.airport_code} - "
                f"{self.destination.city}: {self.destination.airport_code}")
