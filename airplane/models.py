import os.path
import uuid

from django.db import models
from django.utils.text import slugify


class Airline(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def airplane_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/airplanes/", filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=airplane_image_file_path)

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}, capacity: {self.capacity}"
