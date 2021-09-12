from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'chetamdavies@gmail.com',
            'username': 'email',
            'password': 'string1234'
        }
        
    def tearDown(self) -> None:
        return super().tearDown()