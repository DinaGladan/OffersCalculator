from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from datetime import datetime

from account.models import User
from products.models import Product
from settings.models import Tenant
from ..models import Customer, Offer


class Invoice(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("canceled", "Canceled"),
        ("refunded", "Refunded"),
        ("failed", "Failed"),
    ]

    invoice_number = models.CharField(
        max_length=20, unique=True, blank=True, editable=False
    )

    # STATUS_CHOICES je način da se ograniči vrijednost polja na određeni set
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="sent")
    invoice_note = models.TextField(max_length=1500, null=True, blank=True)
    date_created = models.DateTimeField(  # kad je offer nastao
        default=timezone.now, editable=True, null=True, blank=True
    )
    valid_to = models.DateTimeField(
        default=timezone.now, editable=True, null=True, blank=True
    )
    # jedan invoice moze imat vise proizvoda
    products = models.ManyToManyField(Product, related_name="invoices", blank=True)

    # zbroj cijena svih proizvoda u ponudi
    total = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        editable=False,
        default=Decimal("0.00"),
        null=True,
        blank=True,
    )
    # editable je false jer se automatski racunaju
    total_sum = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        editable=False,
        default=Decimal("0.00"),
        null=True,
        blank=True,
    )
    tax = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=Decimal("0.00"),
        null=True,
        blank=True,
    )
    total_tax = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        default=Decimal("0.00"),
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="invoices_created"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="invoices"
    )
    offer = models.ForeignKey(
        Offer, on_delete=models.DO_NOTHING, related_name="invoices"
    )

    def __str__(self):
        return f"Offer{self.invoice_number}"

    class Meta:  # najnovije ponude prve
        ordering = ["-date_created", "-invoice_number"]

    def calculate_total_price(self):
        if len(self.products.all()) > 0:
            self.total = Decimal(
                sum(product.total_price for product in self.products.all())
            )
        else:
            self.total = Decimal(0.0)

        self.total_tax = self.total * Decimal((self.tax / 100))
        self.total_sum = self.total + self.total_tax

    def save(self, *args, kwargs):
        if not self.invoice_number:
            now = datetime.now()  # uzme "srpqnj 2025"
            current_year_month = now.strftime("%Y%m")  # pretvori u "202507"
            last_invoice = (  # pretrazuje sve ponude koje pocinju s "0-202507"
                Invoice.objects.filter(
                    invoice_number__startswith=f"0-{current_year_month}"
                )
                .order_by("-invoice_number")
                .first()  # uzme zadnju napravljenu za taj mjesec
            )
            if last_invoice:  # ako postoji prethodna ponuda izdvoji njen broj(Npr. 007)
                last_invoice_number = int(last_invoice.invoice_number.split("-")[2])
            else:
                last_invoice_number = 0

            self.invoice_number = (
                f"0-{current_year_month}-{str(last_invoice_number+1).zfill(3)}"
            )
            super(Invoice, self).save(*args, kwargs)

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})
