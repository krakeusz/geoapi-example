from django.contrib.auth.models import User, Group
from rest_framework import serializers
from geoapi.api.models import IpGeolocationData

class IpGeolocationDataSerializer(serializers.Serializer):
    ip = serializers.CharField(max_length=100)
    continent_name = serializers.CharField(read_only=True, max_length=50)
    country_name = serializers.CharField(read_only=True, max_length=100)
    region_name = serializers.CharField(read_only=True, max_length=400)
    city = serializers.CharField(read_only=True, max_length=400)
    zip_code = serializers.CharField(read_only=True, max_length=20)
    latitude = serializers.DecimalField(read_only=True, max_digits=17, decimal_places=15)
    longitude = serializers.DecimalField(read_only=True, max_digits=18, decimal_places=15)

    def create(self, validated_data):
        return IpGeolocationData.objects.create(**validated_data)

