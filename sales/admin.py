from django.contrib import admin

from sales.models import Customer, Invoice, Offer

admin.site.register(Customer)  # registracija modela da ga Django prikaže u admin panelu
admin.site.register(Invoice)
admin.site.register(Offer)
