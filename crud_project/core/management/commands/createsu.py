from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'shubham.pokale2001@gmail.com', 'Qwerty@2001')
            self.stdout.write(self.style.SUCCESS('Superuser created'))