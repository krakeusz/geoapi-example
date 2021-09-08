from django.contrib.auth.models import User, Group
from rest_framework import serializers
from geoapi.api.models import IpGeolocationData

class IpGeolocationDataSerializer(serializers.HyperlinkedModelSerializer):
    details_url = serializers.HyperlinkedIdentityField(
        view_name='geodata-detail',
        lookup_field='ip'
    )

    class Meta:
        model = IpGeolocationData
        fields = ['ip', 'details_url', 'continent_name', 'country_name', 'region_name', 'city', 'zip_code', 'latitude', 'longitude']

