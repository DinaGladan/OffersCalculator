from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from faker import Faker
from django.contrib import messages
from account.models import User
from ..models import Gender, CustomerType, Tenant
from sales.models import Customer, Invoice, Offer
from products.models import Ingredient, Product
from decimal import Decimal


class SystemSettingsView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    template_name = "system_settings.html"

    def post(self, request, *args, **kwargs):

        action = request.POST.get("action")  # unutar requesta procita vrijednost akcije

        if action == "seed":
            self.seed_database()
            messages.success(request, "Database was successfully initialized. ")
        elif action == "clean":
            messages.warning(request, "You can not delete database.")
            # self.clean_databe()
        return redirect("settings: system_settings")

    def clean_database(self):
        for model in [
            Gender,
            CustomerType,
            Tenant,
            Ingredient,
            Product,
            Customer,
            Invoice,
            Offer,
            User,
        ]:
            model.objects.all().delete()

    def seed_database(self):
        faker = Faker()
        if not User.objects.filter(
            email="admin@algebra.pydev"
        ).exists():  # uvijek unutar models trebamo pogledat
            User.objects.create_superuser(  # koje podatke nadopunit
                email="admin@algebra.pydev",
                first_name="Admin",
                last_name="User",
                password="admin",
            )
            messages.success(self.request, "Superuser has been made successfully!")

        # radimo obicne usere, npr 3
        for i in range(3):
            email = f"user{i}@gmail.com"
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    email=email, password=f"{i}{i}{i}{i}{i}{i}{i}{i}"
                )
                messages.success(self.request, f"User {email} has been created. ")

        if not Tenant.objects.exists():
            Tenant.objects.create(name="Some Tenant")
            messages.success(self.request, "Tenant has been created.")

        genders = ["Male", "Female", "Non-binary", "Prefer not to say"]
        for gender in genders:
            Gender.objects.get_or_create(name=gender)
        messages.succes(self.request, "Genders were created.")

        types = ["Company", "Person"]
        for type in types:
            CustomerType.objects.get_or_create(name=type)
        messages.success(self.request, "CustomerTypes were created")

        ingredients = ["Salt", "Sugar", "Flour"]
        for ingredient in ingredients:
            Ingredient.objects.get_or_create(
                name=ingredient,
                code=ingredient[
                    :3
                ].upper(),  # mozemo vidjet unutar models od ingredients
            )
        messages.success(self.request, "Ingredients were created")

        products = ["Bread", "Milk", "Juice"]
        for product in products:
            Product.objects.get_or_create(name=product, code=product[:3].upper())
        messages.success(self.request, "Products were created.")

        for i in range(5):
            first_name = faker.first_name()
            last_name = faker.last_name()

            gender = Gender.objects.order_by(
                "?"
            ).first()  # nasumicni redosljed, uzmi prvog iz tog redosljeda
            customer_type = CustomerType.objects.order_by("?").first()

            Customer.objects.get_or_create(
                name=first_name,
                last_name=last_name,
                vat_id=faker.unique.msisdn()[
                    0:11
                ],  # koliko znamenik, jednostavno ovako ide
                street=faker.street_address(),
                postal_code=faker.postcode(),
                city=faker.city(),
                country=faker.country(),
                gender=gender,
                customer_type=customer_type,
            )
        messages.success(self.request, "Customers have been created.")

        for i in range(5):
            customer = Customer.objects.order_by("?").first()
            created_by = User.objects.filter(is_superuser=True).first()
            tenant = Tenant.objects.first()

            # zasto ne get_or_create
            offer = Offer.objects.create(
                created_by=created_by,
                customer=customer,
                tenant=tenant,
                date_created=faker.date_this_year(),
                valid_to=faker.future_datetime(),
                tax=Decimal("25.0"),
            )

            # potrebni nekakakvi podaci
            products = list(Product.objects.order_by("?")[:3])  # uzmi ih 3
            offer.products.set(products)

            offer.calculate_total_price()
            offer.save

            messages.success(self.request, "Offers have been created")

        for i in range(3):
            customer = Customer.objects.order_by("?").first()
            created_by = User.objects.filter(is_superuser=True).first()
            tenant = Tenant.objects.first()  # njega nema u modelima invoice.py?
            offer = Offer.objects.order_by("?").first()

            invoice = Invoice.objects.create(
                created_by=created_by,
                customer=customer,
                tenant=tenant,
                offer=offer,
                date_created=faker.date_this_year(),
                valid_to=faker.future_datetime(),
                tax=Decimal("0.25"),
            )

            products = list(Product.objects.order_by("?")[:3])
            invoice.products.set(products)

            invoice.calculate_total_price()
            invoice.save()
        messages.success(self.request, "Invoices have been created")
