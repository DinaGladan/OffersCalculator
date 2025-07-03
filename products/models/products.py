from django.db import models
from django.urls import reverse
from decimal import Decimal
from .ingredients import Ingredient


class Product(models.Model):
    name = models.CharField(
        max_length=150, help_text="Product name", null=False, blank=False
    )
    code = models.CharField(
        max_length=20, help_text="Product code", null=False, blank=False
    )
    description = models.CharField(
        max_length=150, help_text="Product description", null=True, blank=True
    )
    base_price = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        default=Decimal("0.00"),
        help_text="Product base price",
        null=True,
        blank=True,
    )
    price_mod = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=Decimal("1.00"),
        help_text="Product base price modificator",
        null=True,
        blank=True,
    )
    fixed_costs = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=Decimal("0.00"),
        help_text="Fixed coasts for product",
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        default=Decimal("1.00"),
        help_text="Product total price",
        null=True,
        blank=True,
    )
    # proizvod može imati više sastojaka (i obrnuto)
    ingredients = models.ManyToManyField(  # ingredients je naziv polja i on povezuje trenutni model (Product) s Ingridient modelom
        Ingredient,
        related_name="products",
        blank=True,  # related name= iz modela Ingredient možeš pozvati .products da bi dobio sve proizvode koji koriste taj sastojak
    )
    # sastojak proizvoda moze bit sam po sebi proizvod
    ingredients_from_products = models.ManyToManyField("Product", blank=True)

    def __str__(self):
        if self.name != "" and self.code is not None:
            return f"({self.name} {self.code})"
        else:
            return super().__str__()

    class Meta:
        ordering = ["name", "code"]

    def get_absolute_url(self):
        return reverse("products-detail", kwargs={"pk": self.pk})

    def calculate_total_price(self):
        if len(self.ingredients.all()) > 0:  # ako proizvod ima bar 1 sastojak
            ingredient_total = Decimal(
                sum(
                    Decimal(ingredient.total_price)
                    for ingredient in self.ingredients.all()
                )
            )
        else:
            ingredient_total = Decimal(0.0)

        if len(self.ingredients_from_products.all()) > 0:
            ingredient_from_products_total = Decimal(
                sum(
                    Decimal(ingredients_from_products.total_price)
                    for ingredients_from_products in self.ingredients_from_products.all()
                )
            )
        else:
            ingredient_from_products_total = Decimal(0.0)

        self.base_price = (
            Decimal(self.fixed_costs)
            + ingredient_total
            + ingredient_from_products_total
        )
        self.total_price = Decimal(self.base_price * self.price_mod)

    def save(self, *args, kwargs):  # args je tuple, kwargs dict
        if not self.pk:  # ako proizvod još ne postoji u bazi
            super(Product, self).save(*args, kwargs)
            self.calculate_total_price()
            # treba super nadodat
        else:
            self.calculate_total_price()
            super(Product, self).save(*args, kwargs)
