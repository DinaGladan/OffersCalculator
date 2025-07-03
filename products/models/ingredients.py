from django.db import models
from django.urls import reverse
from decimal import Decimal

# zelimo da 1 proizvod ima 1 ili vise sastojaka


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150, help_text="Ingredient name", null=False, blank=False
    )
    code = models.CharField(
        max_length=20, help_text="Ingredient code", null=False, blank=False
    )
    # blank je postoji al je prazno (sting smi bit enter)
    # null je da ne postoji, ne moze niti enter
    description = models.CharField(
        max_length=150, help_text="Ingredient description", null=True, blank=True
    )
    base_price = models.DecimalField(
        max_digits=18,  # znamenki
        decimal_places=6,  # decimalna mjesta
        default=Decimal("0.00"),
        help_text="Ingredient price",
        null=True,
        blank=True,
    )
    price_mod = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=Decimal("1.00"),
        help_text="Ingredient price modificator",
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=Decimal("1.00"),
        help_text="Ingredient total price",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.name != "" and self.code is not None:
            return f"{self.name} ({self.code})"
        else:
            return super().__str__()

    # ova podklasa je posebna jer se zove Meta
    # samo jer se tako zove Django ce uvik automatski u nju uc i izvrsit je
    # nije potrebno pozivanje
    # u njoj se radi konfiguracija modela (bitna za Django)
    class Meta:  # to je podklasa, mozemo specificirat postavke
        ordering = ["name", "code"]  # -name bi od nazad ka naprid sortiralo

    # metoda se koristi kad zelimo znat URL
    # reverse je Django funkcija koja trazi url iz urls.py po ruti ingredients-detail
    # i onda vraca URL te rute s IDjem (pk) tog objekta
    def get_absolute_url(self):  # poziva se unutar templatea u HTMLu
        return reverse("ingredients-detail", kwargs={"pk": self.pk})

    def calculate_total_price(self):
        self.total_price = Decimal(self.base_price) * Decimal(self.price_mod)

    # nadjacavamo vec postojecu save metodu koja postoji unutar models.Model
    def save(self, *args, kwargs):
        self.calculate_total_price()  # ovo je nadjacavanje
        super(Ingredient, self).save(*args, kwargs)  # a onda nek na stavi po defaultnoj
