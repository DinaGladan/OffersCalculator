from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# models.TIP_PODATKA


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, extra_fields=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, extra_fields=extra_fields)
        user.set_password(password)
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    # moze bit prazno i nije obavezno
    last_name = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    job_position = models.CharField(max_length=255, default="Employee", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # nacin na koji ce se korisnici prijavljivat
    USERNAME_FIELD = "email"
    # Osim emaila se moraju unijeti i ime i prezime
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
