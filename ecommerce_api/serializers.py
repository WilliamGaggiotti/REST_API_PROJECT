from dataclasses import field, fields
from itertools import product
from rest_framework import serializers 

from ecommerce_api.models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['stock']
    
class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['stock']