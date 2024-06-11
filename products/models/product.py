from django.db import models

from .brand import Brand


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.IntegerField()
