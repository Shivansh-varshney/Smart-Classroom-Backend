import json
from django.test import Client
from .TestData import APITestData
from utils.helpers.auths import verify_token

class HelperFunctionsTests(APITestData):

    def test_01_refresh_token(self):

        self.client.defaults['HTTP_REFRESH_TOKEN'] = self.refresh_token
        response = self.client.post('/api/user/refresh_token/')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Valid User", response.content.decode())
    
    def test_02_refresh_token_with_invalid_token(self):

        self.client.defaults['HTTP_REFRESH_TOKEN'] = "invalid token"
        response = self.client.post('/api/user/refresh_token/')

        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid refresh token", response.content.decode())

    def test_03_verfiy_access_token(self):

        token = self.token.split(' ')[1]
        response = verify_token(token)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Valid User", response.content.decode())

    def test_04_verify_invalid_access_token(self):

        response = verify_token("invalid token")

        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid Token", response.content.decode())

    def test_05_verify_session_without_headers(self):

        self.client.defaults['HTTP_AUTHORIZATION'] = "invalid"
        response = self.client.post('/api/admin/organisation/'
        ,
        content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Authentication header missing", response.content.decode())