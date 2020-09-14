import json
from rest_framework import status

from django.urls import reverse
from .models import *
from .serializers import *
from rest_framework.test import APITestCase
from django.contrib.auth.models import User



class RegisterTestCase(APITestCase):

    '''

    Test Module for Register

    '''

    url = reverse("user:register")


    def test_register(self):
        response = self.client.post(self.url, {'email': 'asd@gmail.com', 'first_name': 'asfdf', 'last_name': 'fdgdg', 'password': 'Taher123', 'confirm_password': 'Taher123', 'phone_number': '9029147471', 'address': 'dfgsdfgfd', 'city': 'fdgfd', 'state': 'fdg', 'country': 'fdgf', 'pin-code': '410206'})
        self.assertEqual(201, response.status_code)





class LoginTestCase(APITestCase):


    '''

    Teat Module for Login

    '''


    url = reverse("user:login")

    def setUp(self):
        self.username = "Taher"
        self.email = "Taher@gmail.com"
        self.password = "Taher123"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "Tahe"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "Tah23"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"email-id": self.email, "password": self.password})
        self.assertEqual(200, response.status_code)




