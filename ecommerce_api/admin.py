from django.contrib import admin

from ecommerce_api import models

admin.site.register(models.Product)
admin.site.register(models.Order)
admin.site.register(models.OrderDetail)
