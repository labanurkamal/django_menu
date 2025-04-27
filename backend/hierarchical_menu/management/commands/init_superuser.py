from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser with predefined credentials."

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@gmail.com'
        password = 'admin'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Superuser user "{username}" password "{password}" created successfully.')
            )
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" password "{password}" already exists.'))
