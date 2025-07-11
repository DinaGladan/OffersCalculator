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
from django.utils.translation import gettext_lazy as _
from ..models import Ingredient


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    paginate_by = 10


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient


class IngredientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ingredient
    fields = "__all__"  # U formi će se prikazati sva polja iz modela Ingredient
    success_url = reverse_lazy("products:ingredients")
    success_message = "Ingredient was created successfully"

    def form_valid(self, form):  # kad korisnik uspješno pošalje formu
        response = super().form_valid(
            form
        )  # automatski sprema novi objekt (self.object) u bazu.
        # Rezultat se sprema u response (to je HttpResponseRedirect koji vodi na success_url
        self.object.total_price = self.object.calculate_total_price()
        self.object.save()
        return response


class IngredientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ingredient
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("products:ingredients")
    success_message = "Ingredient was updated successfully"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.total_price = self.object.calculate_total_price
        self.object.save()
        return response


class IngredientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ingredient
    success_url = reverse_lazy("products:ingredients")
