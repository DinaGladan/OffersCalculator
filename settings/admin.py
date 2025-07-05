from django.contrib import admin

from settings.models import CustomerType, Gender, Tenant

admin.site.register(CustomerType)
admin.site.register(Gender)
admin.site.register(Tenant)
