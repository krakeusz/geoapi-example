from geoapi.api.models import IpGeolocationData
from geoapi.api.serializers import IpGeolocationDataSerializer
from geoapi.settings import IPSTACK_ACCESS_KEY
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
import requests


class IpGeolocationDataList(APIView):
    """
    get:

    Shows a list of all IP Geolocation entries in the system.

    You need to be authenticated with JWT in order to access the API.
    You do this by adding a HTTP header "Authentication: Bearer <your-token>" to your request.
    To get your first token, refer to the token documentation below.

    post:

    Allows adding new geolocation data. You only need to pass the IP or domain name, and the geolocation data
    will be fetched from an external service, and then stored in a database.

    The only required parameter is the 'ip' string.
    For example:

    `{ "ip": "8.8.8.8" }`

    or

    `{ "ip": "google.com" }`

    The geolocation data will be fetched from [ipstack.com](https://ipstack.com)

    You need to be authenticated with JWT in order to access the API.
    You do this by adding a HTTP header "Authentication: Bearer <your-token>" to your request.
    To get your first token, refer to the token documentation below.

    """

    def get(self, request, format=None):
        data = IpGeolocationData.objects.all()
        serializer = IpGeolocationDataSerializer(
            data, many=True, context={'request': request})
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
        try:
            ipstack_response = requests.get(
                url=f"http://api.ipstack.com/{request.data['ip']}", params=ipstack_params, timeout=5)
        except requests.exceptions.RequestException as e:
            return Response(exception=e, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        json_response = ipstack_response.json()
        if ('success' in json_response and json_response['success'] == False):
            print(json_response)
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IpGeolocationDataSerializer(data=self.__get_geolocation_data(
            ipstack_response.json()), context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IpGeolocationDataDetail(APIView):
    """
    get:
    Access details of a single IP Geolocation entry.

    You need to be authenticated with JWT in order to access the API.
    You do this by adding a HTTP header "Authentication: Bearer <your-token>" to your request.
    To get your first token, refer to the token documentation below.

    delete:
    Delete a single IP Geolocation entry.

    You need to be authenticated with JWT in order to access the API.
    You do this by adding a HTTP header "Authentication: Bearer <your-token>" to your request.
    To get your first token, refer to the token documentation below.

    """

    def get_object(self, ip):
        try:
            return IpGeolocationData.objects.get(ip=ip)
        except IpGeolocationData.DoesNotExist:
            raise Http404

    def get(self, request, ip, format=None):
        data = self.get_object(ip)
        serializer = IpGeolocationDataSerializer(
            data, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, ip, format=None):
        data = self.get_object(ip)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([AllowAny])
def geolocation_api_root(request, format=None):
    """
    This is an API that allows storing and showing Geolocation data based on IP or domain name.

    To access the API, you need a JWT token. You can generate it if you have a user account.

    For more, see the [documentation section](docs/).
    """
    return Response({
        'geodata': reverse('geodata-list', request=request, format=format),
        'docs': reverse('swagger-ui', request=request, format=format),
    })
