from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
from payment.models import User, Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        for _ in range(100):
            password = make_password("123test123")
            user, status = User.objects.get_or_create(email=fake.email(),
                                                      phone=fake.phone_number(),
                                                      first_last_name=fake.name(),
                                                      password=password,
                                                      is_staff=True)
            Payment.objects.get_or_create(author=user, payment=100)

        self.stdout.write(self.style.SUCCESS("Создание данных завершено"))
