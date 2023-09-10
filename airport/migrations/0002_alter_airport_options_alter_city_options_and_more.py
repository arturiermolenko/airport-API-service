# Generated by Django 4.2.5 on 2023-09-10 10:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("airport", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="airport",
            options={"ordering": ["city"]},
        ),
        migrations.AlterModelOptions(
            name="city",
            options={
                "ordering": ["country"],
                "verbose_name": "city",
                "verbose_name_plural": "cities",
            },
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"verbose_name": "country", "verbose_name_plural": "countries"},
        ),
    ]