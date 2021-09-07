from geoapi.api.models import IpGeolocationData
from geoapi.api.serializers import IpGeolocationDataSerializer
from geoapi.settings import IPSTACK_ACCESS_KEY
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class IpGeolocationDataList(APIView):
    """
    Shows a list of all IP Geolocation entries in the system.

    To add a new entry, write JSON to the "Content:" section at the bottom, in the following format:

    `{ "ip": "8.8.8.8" }`

    or

    `{ "ip": "google.com" }`

    The geolocation data will be fetched from [ipstack.com](https://ipstack.com)

    The entries can be deleted by going to the single entry - follow the link in the 'details_url' field.
    """

    def get(self, request, format=None):
        data = IpGeolocationData.objects.all()
        serializer = IpGeolocationDataSerializer(data, many=True, context={'request': request})
        return Response(serializer.data)

    def __get_geolocation_data(self, ipstack_data):
        return {
            'ip': ipstack_data['ip'],
            'continent_name': ipstack_data['continent_name'],
            'country_name': ipstack_data['country_name'],
            'region_name': ipstack_data['region_name'],
            'city': ipstack_data['city'],
            'zip_code': ipstack_data['zip'],
            'latitude': ipstack_data['latitude'],
            'longitude': ipstack_data['longitude'],
        }

    def post(self, request, format=None):
        ipstack_params = {
            'access_key': IPSTACK_ACCESS_KEY,
        }
        ipstack_response = requests.get(url=f"http://api.ipstack.com/{request.data['ip']}", params=ipstack_params)
        json_response = ipstack_response.json()
        print(json_response)
        if ('success' in json_response and json_response['success'] == False):
            print(json_response)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = IpGeolocationDataSerializer(data=self.__get_geolocation_data(ipstack_response.json()), context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IpGeolocationDataDetail(APIView):
    def get_object(self, pk):
        try:
            return IpGeolocationData.objects.get(pk=pk)
        except IpGeolocationData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = IpGeolocationDataSerializer(data, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)