import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update a Django superuser from environment variables or command options.'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--force', action='store_true', help='Reset password/email if user already exists')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username'] or os.environ.get('ADMIN_USERNAME', 'admin')
        email = options['email'] or os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = options['password'] or os.environ.get('ADMIN_PASSWORD', 'admin@123')
        force = options['force']

        if not username:
            raise CommandError('Admin username must be set via --username or ADMIN_USERNAME.')
        if not password:
            raise CommandError('Admin password must be set via --password or ADMIN_PASSWORD.')

        user_qs = User.objects.filter(username=username)
        if user_qs.exists():
            admin_user = user_qs.first()
            if not admin_user.is_superuser or not admin_user.is_staff:
                admin_user.is_superuser = True
                admin_user.is_staff = True
            if force:
                admin_user.set_password(password)
                admin_user.email = email
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" already exists.'))
            if force:
                self.stdout.write(self.style.SUCCESS('Password and email updated because --force was used.'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created admin user "{username}".'))
