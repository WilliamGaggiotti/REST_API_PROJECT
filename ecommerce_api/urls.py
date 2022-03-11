from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework import routers

from ecommerce_api import views

router = routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('order', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
