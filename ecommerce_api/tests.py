# Django
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import force_authenticate

import json

#Models
from ecommerce_api.models import Order, OrderDetail, Product
User = get_user_model()

class ProductViewTestCase(TestCase):
    
    def setUp(self):
        client = APIClient()

        user =  User.objects.create(username='cfe', email='hello@cfe.com')
        user.set_password("yeahhhcfe")
        user.save()
        
        user = {
            "username":"cfe",
            "password":"yeahhhcfe"
        }

        response = client.post(
            '/api/token/', 
            user,
            format='json'
        )

        result = json.loads(response.content)
        print('AAAAAAAAAAA'+str(result))



    def test_create_product(self):

        client = APIClient()
        user = User.objects.get(username='cfe')
        client.force_authenticate(user=user)

        test_product = {
            "id": 'test_id',
            "name": 'test_product',
            "price": 10000,
            "stock": 10
        }

        response = client.post(
            '/api/product/', 
            test_product,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', result)
        self.assertIn('name', result)
        self.assertIn('price', result)
        self.assertIn('stock', result)

        # if 'pk' in result:
        #     del result['pk']

        # self.assertEqual(result, test_education)