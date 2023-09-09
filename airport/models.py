from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.country}: {self.name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

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

    def __str__(self):
        return (f"{self.source}({self.source.city}) - "
                f"{self.destination}({self.destination.city})")

    @property
    def code(self):
        return f"{self.source[:3].capitalize()} - " \
               f"{self.destination[:3].capitalize()}"
