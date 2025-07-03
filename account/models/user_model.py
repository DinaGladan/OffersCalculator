from django.db import (
    models,
)  # osnovni modul u Django‑u koji omogućuje definiranje modela baze podataka
from django.contrib.auth.models import (
    AbstractBaseUser,  # Uključuje samo osnovne funkcije autentikacije: password, last_login, is_authenticated()...
    BaseUserManager,  # Klasa koja služi za upravljanje korisnicima: create_user(), create_superuser()
    PermissionsMixin,  # Dodaje polja i metode za autorizaciju: is_superuser, groups, user_permissions
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# models.TIP_PODATKA
# model (tablica) je User, a email, first_name,... su atributi (stupci tablice)
class User(AbstractBaseUser, PermissionsMixin, models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    # blank = True, moze bit prazno i nije obavezno
    last_name = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    job_position = models.CharField(max_length=255, default="Employee", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # nacin na koji ce se korisnici prijavljivat
    # konstante se pisu velikim slovima
    USERNAME_FIELD = "email"
    # Osim emaila se moraju unijeti i ime i prezime (dodatna obavezna polja)
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
