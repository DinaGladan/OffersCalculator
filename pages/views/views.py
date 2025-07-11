from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import (
    ExtractYear,
)  # iz datuma izvlači samo godinu (npr. iz 2025-01-01 izvlači 2025)
from django.shortcuts import render  # prikazuje HTML stranicu s kontekstom
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from settings.models import Tenant
from sales.models import Invoice


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get(self, request, *args, kwargs):
        self.seed_database(
            request
        )  # poziva funkciju za punjenje baze  početnim podacima
        return render(request, self.template_name)

    def seed_database(self, request):
        User = get_user_model()  # dohvaća trenutno aktivni model Usera

        if not User.objects.filter(email="admin@algebra.pydev").exists():
            User.objects.create_superuser(
                email="admin@algebra.pydev",
                first_name="Super",
                last_name="Administrator",
                password="PaS$w0rd!",
            )

        job_positions = ["Employee", "Manager", "CEO"]

        user_data = [
            ("ivan.horvat@algebra.pydev", "Ivan", "Horvat", job_positions[0]),
            ("ana.kovacevic@algebra.pydev", "Ana", "Kovačević", job_positions[0]),
            ("marko.maric@algebra.pydev", "Marko", "Marić", job_positions[0]),
            ("ivana.babic@algebra.pydev", "Ivana", "Babić", job_positions[0]),
            ("petar.juric@algebra.pydev", "Petar", "Jurić", job_positions[0]),
            ("marija.novak@algebra.pydev", "Marija", "Novak", job_positions[0]),
            ("tomislav.raic@algebra.pydev", "Tomislav", "Raić", job_positions[0]),
            ("lucija.peric@algebra.pydev", "Lucija", "Perić", job_positions[1]),
            ("ante.bosnjak@algebra.pydev", "Ante", "Bošnjak", job_positions[1]),
            ("maja.tomic@algebra.pydev", "Maja", "Tomić", job_positions[2]),
        ]
        # Provjerava je li postoje svi korisnici iz user data, ako ne postoje napravi ih
        for email, first_name, last_name, job_position in user_data:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    job_position=job_position,
                    password="Pass",
                    is_staff=True,
                    is_active=True,
                )

        tenant = [
            "Mala firma j.d.o.o",
            "312412412",
            "Ilica 1",
            "10000",
            "Zagreb",
            "Hrvatska",
        ]

        if not Tenant.objects.exists():  # Ako ne postoji tenant
            Tenant.objects.create(
                name=tenant[0],
                vat_id=tenant[1],
                street=tenant[2],
                postal_code=tenant[3],
                city=tenant[4],
                country=tenant[5],
            )


# radimo nekakav graf?
class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # nasljedjuje postojeci kontekst

        invoices = Invoice.objects.filter(
            status="paid"
        ).annotate(  # Dohvaća sve plaćene račune
            year=ExtractYear("data_created")
            .values("year")  # Grupira po godini
            .annotate(
                total=Sum("total_sum").order_by("year")
            )  # računa ukupnu zaradu za svaku godinu i sortira po godini
        )

        years = []  # tu se dodaju godine u kojima su racuni placeni
        earnings = []  # tu cemo dodat zbrojevni iznos za svaku godinu
        for invoice in invoices:
            years.append(invoice["year"])
            earnings.append(float(invoice["total"]))

        context["years"] = years
        context["earnings"] = earnings

        statuses = ["sent", "paid"]
        invoice_totals = (
            Invoice.objects.filter(
                status__in=statuses
            )  # dohvaca samo statuse s vrijednosti sent i ili paid
            .values("status")  # grupira po statusu
            .annotate(total=Sum("total_sum"))  # za svaki status izracuna totalnu sumu
            .order_by("status")
        )

        status_labels = []
        status_totals = []
        status_dict = dict(Invoice.STATUS_CHOICES)  # pretvara status_choices u dict
        for invoice in invoice_totals:
            status_labels.append(status_dict.get(invoice["status"], invoice["status"]))
            status_totals.append(float(invoice["total"]))

        context["status_totals"] = status_totals
        return context


class AboutUsPageView(TemplateView):
    template_name = "pages/about.html"


class ContactUsPageView(TemplateView):
    template_name = "pages/contact_us.html"
