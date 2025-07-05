from django.contrib import admin
from products.models import Ingredient, Product

# Register your models here.

admin.site.register(Product)
admin.site.register(Ingredient)
