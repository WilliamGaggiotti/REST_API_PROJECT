from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.FloatField(blank=False)
    stock = models.DecimalField(blank=False, max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['id']