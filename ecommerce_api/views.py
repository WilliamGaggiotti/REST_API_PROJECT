from crypt import methods
from multiprocessing import context
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ecommerce_api.models import Product
from ecommerce_api.serializers import ProductSerializer, ProductUpdateSerializer, ProductStockSerializer

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
