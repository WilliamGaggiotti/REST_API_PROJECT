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
        user =  User.objects.create(username='user_tests', email='user_test@sda.com')
        user.set_password("acscd15a")
        user.save()
        self.user = user

        user = {
            "username":"user_tests",
            "password":"acscd15a"
        }

        response = client.post(
            '/api/token/', 
            user,
            format='json'
        )

        result = json.loads(response.content)
        token = result['access']
        self.client = APIClient()
        #self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Creo un objeto en la base de datos para trabajar con datos
        self.product = Product.objects.create(
            id='test_id',
            name='test_product',
            price=10000,
            stock=10
        )

    def test_create_product(self):

        test_product = {
            "id": 'test_id_c',
            "name": 'test_product_c',
            "price": 10000,
            "stock": 10
        }

        response = self.client.post(
            '/api/product/', 
            test_product,
            format='json'
        )
        
        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('test_id_c', result['id'])
        self.assertEqual('test_product_c', result['name'])
        self.assertEqual(10000.0, result['price'])
        self.assertEqual(10, result['stock'])

    def test_update_product(self):

        test_product_update = {
            "name": "test_product_u",
            "price": 5000
        }
        
        response = self.client.put(
            '/api/product/test_id/', 
            test_product_update,
            format='json'
        )
        
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_product_u', result['name'])
        self.assertEqual(5000.0, result['price'])

    def test_partial_update_product(self):

        test_product_update = {
            "name": "test_product_u"
        }
        
        response = self.client.patch(
            '/api/product/test_id/', 
            test_product_update,
            format='json'
        )
        
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_product_u', result['name'])
        
    def test_get_product(self):

        response = self.client.get(
            '/api/product/test_id/',
            format='json'
        )
        
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test_id', result['id'])
        self.assertEqual('test_product', result['name'])
        self.assertEqual(10000.0, result['price'])
        self.assertEqual(10, result['stock'])
    
    def test_list_product(self):

        response = self.client.get(
            '/api/product/',
            format='json'
        )
        
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(result))
        self.assertEqual('test_id', result[0]['id'])
        self.assertEqual('test_product', result[0]['name'])
        self.assertEqual(10000.0, result[0]['price'])
        self.assertEqual(10, result[0]['stock'])

    def test_delete_product(self):

        response = self.client.delete(
            '/api/product/test_id/',
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        prod_exists = Product.objects.filter(pk='test_id')
        self.assertFalse(prod_exists)


    def test_update_stock(self):

        test_stock = {
            "stock": 3
        }

        response = self.client.post(
            '/api/product/test_id/update_stock/', 
            test_stock,
            format='json'
        )

        result = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, result['new stock'])

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(3, result['stock'])

class OrderViewTestCase(TestCase):
    
    def setUp(self):

        client = APIClient()
        user =  User.objects.create(username='user_tests', email='user_test@sda.com')
        user.set_password("acscd15a")
        user.save()
        self.user = user

        user = {
            "username":"user_tests",
            "password":"acscd15a"
        }

        response = client.post(
            '/api/token/', 
            user,
            format='json'
        )

        result = json.loads(response.content)
        token = result['access']
        self.client = APIClient()
        #self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Creo un objeto en la base de datos para trabajar con datos
        self.product_1 = Product.objects.create(
            id='test_id_1',
            name='test_product_1',
            price=10000,
            stock=10
        )
        self.product_2 = Product.objects.create(
            id='test_id_2',
            name='test_product_2',
            price=10000,
            stock=10
        )
        self.order = Order.objects.create(
            date_time="2012-04-21T23:25:43Z"
        )
        self.order_detail_1 = OrderDetail.objects.create(
            order=self.order,
            product=self.product_1,
            cuantity=5
        )
        self.order_detail_2 = OrderDetail.objects.create(
            order=self.order,
            product=self.product_2,
            cuantity=5
        )

    def test_create_order(self):

        test_order = {
             "order_details": [
                 {"cuantity":11, "product":"test_id_1" },
                 {"cuantity":6, "product":"test_id_2" }
                 ],
             "date_time": "2012-04-21T23:25:43Z"
            }

        response = self.client.post(
            '/api/order/', 
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #400 por no haber stock
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_order['order_details'][0]['cuantity']=6
        test_order['order_details'][0]['product']='test_id_2'

        response = self.client.post(
            '/api/order/', 
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #400 por poner el mismo producto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        test_order['order_details'][0]['product']='test_id_1'

        response = self.client.post(
            '/api/order/', 
            test_order,
            format='json'
        )
        result = json.loads(response.content)
        #201 ya que ahora el stock y los productos estan bien
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('2012-04-21T23:25:43Z', result['date_time'])
        self.assertEqual(6, result['order_details'][0]['cuantity'])
        self.assertEqual('test_id_1', result['order_details'][0]['product'])
        self.assertEqual(6, result['order_details'][1]['cuantity'])
        self.assertEqual('test_id_2', result['order_details'][1]['product'])

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id_1/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(4, result['stock'])

        response = self.client.get(
            '/api/product/test_id_2/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(4, result['stock'])

    def test_get_order(self):

        response = self.client.get(
            '/api/order/{}/'.format(self.order.get_id()),
            format='json'
        )
        
        result = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('2012-04-21T23:25:43Z', result['date_time'])
        self.assertEqual(5, result['order_details'][0]['cuantity'])
        self.assertEqual('test_id_1', result['order_details'][0]['product'])
        self.assertEqual(5, result['order_details'][1]['cuantity'])
        self.assertEqual('test_id_2', result['order_details'][1]['product'])
    
    def test_delete_order(self):

        response = self.client.delete(
            '/api/order/{}/'.format(self.order.get_id()),
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        order_exists = Order.objects.filter(pk=self.order.get_id())
        self.assertFalse(order_exists)

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id_1/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(15, result['stock'])

        response = self.client.get(
            '/api/product/test_id_2/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(15, result['stock'])
    
    def test_update_order(self):
        
        test_order = {
             "order_details": [
                 {"id": self.order_detail_1.get_id(), "cuantity":16, "product":"test_id_1" },
                 {"id":self.order_detail_2.get_id(), "cuantity":6, "product":"test_id_2" }
                 ],
             "date_time": "2013-04-21T23:25:43Z"
            }
        
        response = self.client.put(
            '/api/order/{}/'.format(self.order.get_id()),
            test_order,
            format='json'
        )
        
        result = json.loads(response.content)
        #400 por no haber stock
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_order['order_details'][0]['cuantity']=6
        test_order['order_details'][0]['product']='test_id_2'

        response = self.client.put(
            '/api/order/{}/'.format(self.order.get_id()),
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #400 por poner el mismo producto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_order['order_details'][0]['product']='test_id_1'

        response = self.client.put(
            '/api/order/{}/'.format(self.order.get_id()),
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #200 ya que ahora el stock y los productos estan bien
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual('2013-04-21T23:25:43Z', result['date_time'])
        self.assertEqual(6, result['order_details'][0]['cuantity'])
        self.assertEqual('test_id_1', result['order_details'][0]['product'])
        self.assertEqual(6, result['order_details'][1]['cuantity'])
        self.assertEqual('test_id_2', result['order_details'][1]['product'])

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id_1/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(9, result['stock'])

        response = self.client.get(
            '/api/product/test_id_2/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(9, result['stock'])
        
    def test_add_order_details(self):

        order = Order.objects.create(
            date_time="2012-04-21T23:25:43Z"
        )
        test_order = {"order_details": [
                 {"cuantity":11, "product":"test_id_1" },
                 {"cuantity":6, "product":"test_id_2" }
                 ]
        }
        response = self.client.post(
            '/api/order/{}/add_order_details/'.format(order.get_id()),
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #400 por no haber stock
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_order['order_details'][0]['cuantity']=6
        test_order['order_details'][0]['product']='test_id_2'
        
        response = self.client.post(
            '/api/order/{}/add_order_details/'.format(order.get_id()),
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #400 por poner el mismo producto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        test_order['order_details'][0]['product']='test_id_1'

        response = self.client.post(
            '/api/order/{}/add_order_details/'.format(order.get_id()),
            test_order,
            format='json'
        )

        result = json.loads(response.content)
        #200 ya que ahora el stock y los productos estan bien
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(6, result['order_details'][0]['cuantity'])
        self.assertEqual('test_id_1', result['order_details'][0]['product'])
        self.assertEqual(6, result['order_details'][1]['cuantity'])
        self.assertEqual('test_id_2', result['order_details'][1]['product'])

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id_1/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(4, result['stock'])

        response = self.client.get(
            '/api/product/test_id_2/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(4, result['stock'])

    def test_remove_order_details(self):

        test_order = {"order_detail_ids": [self.order_detail_1.get_id()]
        }

        response = self.client.post(
            '/api/order/{}/remove_order_details/'.format(self.order.get_id()),
            test_order,
            format='json'
        )
        
        result = json.loads(response.content)
        #200 ya que ahora el stock y los productos estan bien
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

        #verificamos si se borro
        response = self.client.get(
            '/api/order/{}/'.format(self.order.get_id()),
            format='json'
        )
        
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(result['order_details']))
        self.assertEqual(self.order_detail_2.get_id(), result['order_details'][0]['id'])

        #verificamos si realmente se actualizo el stock
        response = self.client.get(
            '/api/product/test_id_1/',
            format='json'
        )
        result = json.loads(response.content)
        self.assertEqual(15, result['stock'])

    def test_list_order(self):

        response = self.client.get(
            '/api/order/',
            format='json'
        )
        
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(result))
        self.assertEqual(self.order.get_id(), result[0]['id'])
