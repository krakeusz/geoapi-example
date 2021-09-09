from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class IpGeolocationTests(APITestCase):
    fixtures = ['testing.json']

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
    
    def __add_new_token_to_authorization_header(self, client):
        """
        After this call, all calls to the client methods will be authorized by a new JSON Web Token.
        """
        access_token, _ = self.__get_new_token_pair()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_root_view_contains_link_to_documentation(self):
        url = reverse('root')
        response = self.client.get(url)
        self.assertContains(response, '/docs/', status_code=status.HTTP_200_OK)

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

    def test_refreshing_access_token(self):
        url = reverse('token_refresh')
        _, refresh_token = self.__get_new_token_pair()
        response = self.client.post(url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in json.loads(response.content))
    
    def test_fetching_list_of_geodata(self):
        url = reverse('geodata-list')
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.get(url, format='json')
        self.assertContains(response, 'Split-Dalmatia', status_code=status.HTTP_200_OK)
    
    def test_list_of_geodata_requires_authentication(self):
        url = reverse('geodata-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_fetching_individual_geodata(self):
        ip = '8.8.4.4'
        url = reverse('geodata-detail', kwargs={'ip': ip})
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.get(url, format='json')
        self.assertContains(response, ip, status_code=status.HTTP_200_OK)
    
    def test_posting_new_geodata_ipv6(self):
        ipv6 = '2001:4860:4860::8888'
        url = reverse('geodata-list')
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.post(url, {'ip': ipv6}, format='json')
        self.assertContains(response, ipv6, status_code=status.HTTP_201_CREATED)
    
    def test_posting_new_geodata_ipv4(self):
        ipv4 = '9.9.9.9'
        url = reverse('geodata-list')
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.post(url, {'ip': ipv4}, format='json')
        self.assertContains(response, ipv4, status_code=status.HTTP_201_CREATED)

        # verify that the newly added data is accessible
        response = self.client.get(reverse('geodata-detail', kwargs={'ip': ipv4}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_posting_new_geodata_domain_name(self):
        domain_name = 'amazon.com'
        url = reverse('geodata-list')
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.post(url, {'ip': domain_name}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_deleting_geodata(self):
        ip = '8.8.4.4'
        url = reverse('geodata-detail', kwargs={'ip': ip})
        self.__add_new_token_to_authorization_header(self.client)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # verify that the data is inaccessible
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


