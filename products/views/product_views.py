# # 1.nacin FBV
# def product_list(request):
#     products = Product.objects.all()  # uziamo proizvode iz baze
#     # render funkcija vraća HTML stranicu sa ubačenim podacima (products) u kontekst
#     return render(request, "products/product_list.html", {"products": products})


# # 2.nacin za kompleksije zadatke CBV
# class ProductListView(ListView):  # za prikaz liste, za prikaz objekatabi bio ClientView
#     model = Product  # odakle iz baze zelimo uzet podatke (iz Product)
#     template_name = "products/product_list.html"  # putanja di ih zelimo ubacit
#     context_object_name = "products"  # pod kojim imenom cemo ih ubacit


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy("products:products")
    success_message = "Product was created successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.total_price = self.object.calculate_total_price
        self.object.save()
        return response


class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("products:products")
    success_message = "Product was updated successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.total_price = self.object.calculate_total_price
        self.object.save()
        return response


class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("products:products")
