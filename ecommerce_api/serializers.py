from dataclasses import field, fields
from itertools import product
from venv import create
from rest_framework import serializers 

from ecommerce_api.models import Product, Order, OrderDetail

###################################
#      Products Serializers       #
###################################

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['stock','id']
    
class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['stock']


############################################
#     OrderDetailSerializer Serializers    #
############################################

class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderDetail
        #depth = 1
        exclude = ['order']


###################################
#       Order Serializers         #
###################################

class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True)
    total_to_pay = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        only_read_fields = ('total_to_pay',)

    def get_total_to_pay(self, order):
        divisa = self.context['request'].GET.get('divisa')
        if divisa == 'usd':
            return order.get_total_usd()
        return order.get_total()

    def create(self, valdiate_date):
        order_details_data = valdiate_date.pop('order_details')
        order = super().create(valdiate_date)
        for order_detail_data in order_details_data:
            OrderDetail.objects.create(order=order, **order_detail_data)
        
        return order

    def update(self, instance, valdiate_date):
        order_details_data = valdiate_date.pop('order_details') if 'order_details' in valdiate_date.keys() else []
        order_details = list(instance.order_details.all())
        order = super().update(instance, valdiate_date)
        order_details_updated = []
        for order_detail_data in order_details_data:
            order_detail = order_details.pop(0)
            order_detail.set_cuantity(order_detail_data['cuantity'])
            order_detail.set_product(order_detail_data['product'])
            order_details_updated.append(order_detail)

        OrderDetail.objects.bulk_update(order_details_updated, ['cuantity','product'])

        return order

class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
