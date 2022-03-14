from enum import unique
from pyexpat import model
from django.db import models

from functools import reduce
import requests

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()#(max_digits=7, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        ordering = ['id']

    def set_stock(self, new_stock):
        self.stock = new_stock

    def get_stock(self):
        return self.stock
    
    def get_id(self):
        return self.id
    
    def get_price(self):
        return self.price

class Order(models.Model):
    date_time = models.DateTimeField()

    class Meta:
        ordering = ['id']

    def get_id(self):
        return self.id

    def get_total(self):
        order_details = OrderDetail.objects.filter(order=self.id).select_related('product')
        
        #return reduce(lambda a, b: (a.get_cuantity() * a.product.get_price()) + (b.get_cuantity() * b.product.get_price()), order_details)
        return sum([order_detail.get_cuantity() * order_detail.product.get_price() for order_detail in order_details])

    def get_total_usd(self):
        requests_api = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        if requests_api.status_code == 200:
            structured_data = {element['casa']['nombre']:element['casa']['venta'] for element in requests_api.json()}

        return round(self.get_total() / float(structured_data['Dolar Blue'].replace(',', '.')), 2)

class OrderDetail(models.Model):
    cuantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')

    class Meta:
        ordering = ['id']

    def set_cuantity(self, new_cuantity):
        self.cuantity = new_cuantity

    def set_product(self, new_product):
        self.product = new_product

    def get_cuantity(self):
        return self.cuantity

    def get_product(self):
        return self.product

    def get_id(self):
        return self.id