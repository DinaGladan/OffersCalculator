from django.contrib import admin

from sales.models import Customer, Invoice, Offer
from settings.models import CustomerType, Gender, Tenant
from products.models import Ingredient, Product
from account.models import User


admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(Offer)
admin.site.register(CustomerType)
admin.site.register(Gender)
admin.site.register(Tenant)
admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(User)
