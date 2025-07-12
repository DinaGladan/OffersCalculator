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
from ..models import Tenant


class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    paginate_by = 10


class TenantDetailView(LoginRequiredMixin, DetailView):
    model = Tenant


class TenantUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tenant
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_message = "Tenant has been updated!"
    success_url = "settings:tenants"
