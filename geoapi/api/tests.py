from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class IpGeolocationTests(APITestCase):
    def test_swagger_documentation_is_visible_to_public(self):
        url = reverse('swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getting_jwt_access_token(self):
        username = 'john'
        password = 'johnpassword'
        User.objects.create_user(username, 'lennon@thebeatles.com', password)
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in json.loads(response.content))
    
    def __get_new_token_pair(self):
        """
        Returns a pair: a new JWT access token and a new JWT refresh token, for a temporary user.
        """
        username = 'johnny'
        password = 'johnpassword'
        User.objects.create_user(username, 'johnny@thebeatles.com', password)
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': username, 'password': password}, format='json')
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return (response_json['access'], response_json['refresh'])

    def test_refreshing_access_token(self):
        url = reverse('token_refresh')
        _, refresh_token = self.__get_new_token_pair()
        response = self.client.post(url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in json.loads(response.content))
