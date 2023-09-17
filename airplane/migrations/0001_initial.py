# Generated by Django 4.2.5 on 2023-09-17 16:38

import airplane.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airline",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="AirplaneType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Airplane",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("rows", models.IntegerField()),
                ("seats_in_row", models.IntegerField()),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=airplane.models.airplane_image_file_path
                    ),
                ),
                (
                    "airline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airplane.airline",
                    ),
                ),
                (
                    "airplane_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="airplane.airplanetype",
                    ),
                ),
            ],
        ),
    ]
