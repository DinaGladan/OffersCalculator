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
from ..models import CustomerType


class CustomerTypeListView(LoginRequiredMixin, ListView):
    model = CustomerType
    paginate_by = 10


class CustomerTypeDetailView(LoginRequiredMixin, DetailView):
    model = CustomerType


class CustomerTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CustomerType
    fields = "__all__"
    success_url = reverse_lazy("settings: customer_types")
    success_message = "Customer type has been added successfully!"


class CustomerTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomerType
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("settings: customer_types")
    success_message = "Customer types have been updated successfully!"


class CustomerTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomerType
    success_url = reverse_lazy("settings: customer_types")
