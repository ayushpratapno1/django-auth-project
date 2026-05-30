from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.getenv("SUPERUSER_USERNAME")
        email = os.getenv("SUPERUSER_EMAIL")
        password = os.getenv("SUPERUSER_PASSWORD")

        if not username or not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Superuser environment variables not found."
                )
            )
            return

        user = User.objects.filter(username=username).first()

        if user:

            if user.is_superuser:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Superuser already exists."
                    )
                )
                return

            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    "Existing user promoted to superuser."
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Superuser created successfully."
            )
        )