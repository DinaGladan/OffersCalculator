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
from ..models import Gender


class GenderListView(LoginRequiredMixin, ListView):
    model = Gender
    paginate_by = 10


class GenderDetailView(LoginRequiredMixin, DetailView):
    model = Gender


class GenderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Gender
    fields = "__all__"
    success_url = reverse_lazy("settings:genders")
    success_message = "Gender has been added successfully!"


class GenderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Gender
    fields = "__all__"
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("settings:genders")
    success_message = "Gender has been added successfully!"


class GenderDeleteView(LoginRequiredMixin, DeleteView):
    model = Gender
    success_url = reverse_lazy("settings:genders")
