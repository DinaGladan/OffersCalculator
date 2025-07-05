from django.shortcuts import render
from django.views.generic import ListView
from ..models import Product


# 1.nacin FBV
def product_list(request):
    products = Product.objects.all()  # uziamo proizvode iz baze
    # render funkcija vraća HTML stranicu sa ubačenim podacima (products) u kontekst
    return render(request, "products/product_list.html", {"products": products})


# 2.nacin za kompleksije zadatke CBV
class ProductListView(ListView):  # za prikaz liste, za prikaz objekatabi bio ClientView
    model = Product  # odakle iz baze zelimo uzet podatke (iz Product)
    template_name = "products/product_list.html"  # putanja di ih zelimo ubacit
    context_object_name = "products"  # pod kojim imenom cemo ih ubacit
