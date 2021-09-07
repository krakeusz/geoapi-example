from geoapi.api.models import IpGeolocationData
from geoapi.api.serializers import IpGeolocationDataSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class IpGeolocationDataList(APIView):

    def get(self, request, format=None):
        data = IpGeolocationData.objects.all()
        serializer = IpGeolocationDataSerializer(data, many=True)
        return Response(serializer.data)

class IpGeolocationDataDetail(APIView):
    def get_object(self, pk):
        try:
            return IpGeolocationData.objects.get(pk=pk)
        except IpGeolocationData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        data = self.get_object(pk)
        serializer = IpGeolocationDataSerializer(data)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        data = self.get_object(pk)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)