import json
from .TestData import APITestData

class UserAddressAPITests(APITestData):

    def test_01_get_user_address(self):
        """Test get user address"""

        response = self.client.post("/api/user/address/", {
            "user_id": self.user.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("User address found", response.content.decode())
    
    def test_02_get_user_address_with_invalid_user(self):
        """Test get user address with invalid"""

        response = self.client.post("/api/user/address/", {
            "user_id": 99
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.content.decode())
    
    def test_03_get_user_address_with_invalid_request_method(self):
        """Test get user address with invalid request method"""

        response = self.client.get("/api/user/address/", {
            "user_id": self.user.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_04_get_user_address_with_missing_details(self):
        """Test get user address with missing_details"""

        response = self.client.post("/api/user/address/", {
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("user_id is missing", response.content.decode())
    
    def test_05_get_user_address_when_they_do_not_have_address(self):
        """Test get user address with invalid request method"""

        response = self.client.post("/api/user/address/", {
            "user_id": self.user2.id
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("User does not have address", response.content.decode())

    def test_06_create_user_address(self):
        """Test create user address"""

        response = self.client.post("/api/admin/address/create/", {
            'user_id': self.user2.id,
            'house_number': "123A",
            'street': "Main Street",
            'city': "New York",
            'district': "Manhattan",
            'state': "NY",
            'country': "USA",
            'zipcode': 10001
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Address saved successfully", response.content.decode())
    
    def test_07_create_user_address_with_missing_details(self):
        """Test create user address"""

        response = self.client.post("/api/admin/address/create/", {
            'user_id': self.user2.id,
            'house_number': "123A",
            'street': "Main Street",
            'city': "New York",
            'district': "Manhattan",
            'zipcode': 10001
        },content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_08_create_user_address_with_invalid_admin(self):
        """Test create user address"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/address/create/", {
            'user_id': self.user2.id,
            'house_number': "123A",
            'street': "Main Street",
            'city': "New York",
            'district': "Manhattan",
            'state': "NY",
            'country': "USA",
            'zipcode': 10001
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())

    def test_09_create_address_for_non_existing_user(self):
        """Test create user address"""
    
        response = self.client.post("/api/admin/address/create/", {
            'user_id': 99,
            'house_number': "123A",
            'street': "Main Street",
            'city': "New York",
            'district': "Manhattan",
            'state': "NY",
            'country': "USA",
            'zipcode': 10001
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("User not found", response.content.decode())
    
    def test_10_create_address_with_invalid_request_method(self):
        """Test create user address"""
    
        response = self.client.get("/api/admin/address/create/", {
            'user_id': 99,
            'house_number': "123A",
            'street': "Main Street",
            'city': "New York",
            'district': "Manhattan",
            'state': "NY",
            'country': "USA",
            'zipcode': 10001
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())
    
    def test_11_create_address_for_unhandled_exceptions(self):
        """Test create user address"""
    
        response = self.client.post("/api/admin/address/create/", {
            """'subject_id': self.subject.id,
            'new_details': {
                'semester': 4
            }"""
        }, content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertIn("Something went wrong", response.content.decode())
    
    def test_12_update_address(self):
        """Test update address"""

        response = self.client.post("/api/admin/address/update/", {
            "address_id": self.address.id,
            "new_details": {
                'house_number': "13B",
                'street': "Side Street",
                'city': "York New",
                'district': "Nattahnam",
                'state': "YN",
                'country': "ASU",
                'zipcode': 10001
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Address updated successfully", response.content.decode())
    
    def test_13_update_address_with_invalid_request_method(self):
        """Test update address"""

        response = self.client.get("/api/admin/address/update/", {
            "address_id": self.address.id,
            "new_details": {
                'house_number': "13B",
                'street': "Side Street",
                'city': "York New",
                'district': "Nattahnam",
                'state': "YN",
                'country': "ASU",
                'zipcode': 10001
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 405)
        self.assertIn("Invalid request method", response.content.decode())

    def test_14_update_address_with_missing_details(self):
        """Test update address"""

        response = self.client.post("/api/admin/address/update/", {
            "new_details": {
                'house_number': "13B",
                'street': "Side Street",
                'city': "York New",
                'district': "Nattahnam",
                'state': "YN",
                'country': "ASU",
                'zipcode': 10001
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("one or more fields missing", response.content.decode())
    
    def test_15_update_user_in_address(self):
        """Test update address"""

        response = self.client.post("/api/admin/address/update/", {
            "address_id": self.address.id,
            "new_details": {
                'user': self.user2.id
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertIn("User can not be changed", response.content.decode())
    
    def test_16_update_invalid_field_in_address(self):
        """Test update address"""

        response = self.client.post("/api/admin/address/update/", {
            "address_id": self.address.id,
            "new_details": {
                'volume': '100'
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn("volume is invalid field", response.content.decode())
    
    def test_17_update_non_existing_address(self):
        """Test update address"""

        response = self.client.post("/api/admin/address/update/", {
            "address_id": 99,
            "new_details": {
                'house_number': "13B",
                'street': "Side Street",
                'city': "York New",
                'district': "Nattahnam",
                'state': "YN",
                'country': "ASU",
                'zipcode': 10001
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn("Address not found", response.content.decode())
    
    def test_18_update_address_with_invalid_admin(self):
        """Test update address with invalid admin"""

        response = self.client.post('/api/user/login/', 
        data = {
            'email': 'testuser3@gmail.com',
            'password': 'password'
        }, content_type='application/json')

        self.token = f"Bearer {response.headers.get('ACCESS-TOKEN')}"
        if self.token:
            self.client.defaults['HTTP_AUTHORIZATION'] = self.token
            self.client.defaults['HTTP_USER_ID'] = str(self.user3.id)

        response = self.client.post("/api/admin/address/update/", {
            "address_id": self.address.id,
            "new_details": {
                'house_number': "13B",
                'street': "Side Street",
                'city': "York New",
                'district': "Nattahnam",
                'state': "YN",
                'country': "ASU",
                'zipcode': 10001
            }
        }, content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertIn("unauthorized access", response.content.decode())
