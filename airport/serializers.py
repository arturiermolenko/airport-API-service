from rest_framework import serializers

from .models import Country, City, Airport, Route


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(
        source="country.name",
        read_only=True
    )

    class Meta:
        model = City
        fields = ("id", "name", "country_name")


class AirportSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(
        source="city.name",
        read_only=True
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "city_name")


class AirportCreateSerializer(AirportSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "code", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_name = serializers.CharField(
        source="source.name",
        read_only=True
    )
    destination_name = serializers.CharField(
        source="destination.name",
        read_only=True
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "code",
            "source_name",
            "destination_name",
            "distance"
        )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "code", "source", "destination", "distance")
