from django.contrib import admin

from products.models import Product, Brand

admin.site.register(Product)
admin.site.register(Brand)

