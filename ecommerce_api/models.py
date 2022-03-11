from enum import unique
from pyexpat import model
from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    stock = models.DecimalField(max_digits=7, decimal_places=2)

    def set_stock(self, new_stock):
        self.stock = new_stock

    def get_stock(self):
        return self.stock
    
    def get_id(self):
        return self.id

    class Meta:
        ordering = ['id']

class Order(models.Model):
    date_time = models.DateTimeField()

    class Meta:
        ordering = ['id']

class OrderDetail(models.Model):
    cuantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details')

    def set_cuantity(self, new_cuantity):
        self.cuantity = new_cuantity

    def set_product(self, new_product):
        self.product = new_product

    class Meta:
        ordering = ['id']