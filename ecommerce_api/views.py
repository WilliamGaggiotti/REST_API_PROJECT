from crypt import methods
from itertools import product
from multiprocessing import context
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from ecommerce_api.models import Order, OrderDetail, Product
from ecommerce_api.utils import ProductUtil
from ecommerce_api.serializers import ProductSerializer, ProductUpdateSerializer, ProductStockSerializer, OrderListSerializer,\
                                        OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    #serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if (self.action in ['partial_update','update']):
            return ProductUpdateSerializer
        elif (self.action == 'update_stock'):
            return ProductStockSerializer
        else:
            return ProductSerializer
    
    @action(methods=['POST'], detail=True)
    def update_stock(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            product.set_stock(serializer.validated_data['stock'])
            product.save()
            return Response({'new stock': serializer.validated_data['stock']},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if (self.action in ['list']):
            return OrderListSerializer
        else:
            return OrderSerializer

    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            order_details = serializer.validated_data['order_details']
            if any([prod_and_cant['product'].get_stock() < prod_and_cant['cuantity'] for prod_and_cant in order_details]):
                raise serializers.ValidationError('No hay stock disponible de algunos de los productos solicitados')
            else:
                #Actualizamos el stock de los productos
                ProductUtil.update_product_stock(order_details, -1)
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        order = self.get_object()
        order_details = OrderDetail.objects.filter(order=pk).select_related('product')
        prod_and_cants = [ {"product":order_detail.product, "cuantity":order_detail.cuantity}for order_detail in order_details]
        #Actualizamos el stock de los productos
        ProductUtil.update_product_stock(prod_and_cants)
        self.perform_destroy(order)
        return Response('Orden eliminada exitosamente.', status=status.HTTP_200_OK)