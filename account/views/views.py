# isto sto i get post put delete
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from ..models import User

# Django-ova klasa za validaciju username-a provjerava je li korisničko ime
# sadrži dozvoljene karaktere – slova, brojevi, donje crte (_), bez razmaka i specijalnih znakova
username_validator = UnicodeUsernameValidator()


# ovoe samo read R
# LoginRequiredMixin - osigurava da samo ulogoirani korisnici mogu pristupiti
class UserListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 10  # koliko je po stranici prikazanih korisnika
    template_name = "registration/user_list.html"
    # zasto nismo postavili context_object_name?


# C
class UserCreateForm(
    UserCreationForm
):  # nasljedjuje djangovu formu za kreiranje korisnika
    # prosirujemo je s emailom, first and last nameom
    email = forms.EmailField(
        required=True,
        help_text="Email adress.",
        widget=(forms.TextInput()),  # mozda bolje EmailInput()
    )
    first_name = forms.CharField(
        required=True, help_text="First name.", widget=(forms.TextInput())
    )
    last_name = forms.CharField(
        required=True, help_text="Last name.", widget=(forms.TextInput())
    )
    # automatski usporedjuje jesu li ova 2 passworda ista
    # _() funkcija koja prevodi tekst na korisnikov
    password1 = forms.CharField(label=_("Password"), widget=(forms.PasswordInput()))
    password2 = forms.CharField(
        # label-pored polja, help_text-ispod polja
        label=_("Password Confirmation"),
        widget=(forms.PasswordInput()),
    )

    # klasa Meta se koristi unutar forme (UserCreateForm)
    # kako bi Django znao s kojim modelom forma radi
    # i koja polja želiš uključiti u formu.
    class Meta:
        model = User
        fields = (  # atributi tablice User
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "description",
            "job_position",
            "is_activate",
            "is_staff",
            "is_superuser",
        )


# C
# forma je pravljenje nove stranice
class UserCreateView(
    LoginRequiredMixin, CreateView
):  # CreateView- kreira objekat u bazi ako je sve ispravno.
    form_class = UserCreateForm  # iskoristi ovu formu da bi se napravio view
    template_name = "registration/user_form.html"
    success_url = reverse_lazy(
        "account:users"  # ako se ovo uspjesno napravi vrati ga na URL s imenom account:users
    )


# U
class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(
        required=True, help_text="Email adress.", widget=(forms.TextInput)
    )
    first_name = forms.CharField(
        required=True, help_text="First Name.", widget=(forms.TextInput)
    )
    last_name = forms.CharField(
        required=True, help_text="Last Name.", widget=(forms.TextInput)
    )
    new_password = forms.CharField(
        label=_("New Password"), widget=(forms.PasswordInput()), required=False
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "description",
            "job_position",
            "is_activate",
            "is_staff",
            "is_superuser",
            "new_password",
        )


# U
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User  # ovdje je potreban rec koji model se azurira jer sad vec postoji
    form_class = UserUpdateForm
    template_name = "registration/user_update_form.html"
    success_url = reverse_lazy("account:users")

    # radimo promjenu lozinke, nadjacavamo vec postojecu
    def form_valid(self, form):  # kad su svi podaci validni se poziva
        response = super().form_valid(form)  # pokreće regularno ažuriranje korisnika
        new_password = form.cleaned_data.get(
            "new_password"  # proverava je li je korisnik unio novu lozinku
        )
        if new_password:  # self.object je nas User
            self.object.set_password(new_password)
            self.object.save()  # spremi u bazi
            messages.success(
                self.request,
                f"Password for user {self.object.first_name} has been changed successfully.",
            )
        else:
            messages.success(
                self.request,
                f"User{self.object.first_name} has been updated successfully.",
            )
        return response


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "registration/user_confirm_delete.html"
    success_url = reverse_lazy("account:users")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("pages:index")
