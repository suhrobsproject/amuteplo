import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Hosting uchun server: migrate, collectstatic, so'ng waitress (SOCKET yoki PORT)"

    def handle(self, *args, **options):
        call_command('migrate', interactive=False, verbosity=1)
        call_command('collectstatic', interactive=False, verbosity=0)
        self.ensure_superuser()

        from waitress import serve
        from teplo.wsgi import application

        sock = os.environ.get('SOCKET')
        if sock:
            if os.path.exists(sock):
                os.remove(sock)
            self.stdout.write(f"Serving on unix:{sock}")
            serve(application, unix_socket=sock, unix_socket_perms='666', threads=8)
        else:
            port = int(os.environ.get('PORT', 8000))
            self.stdout.write(f"Serving on 127.0.0.1:{port}")
            serve(application, host='127.0.0.1', port=port, threads=8)

    def ensure_superuser(self):
        # .env da ADMIN_USERNAME va ADMIN_PASSWORD bo'lsa va admin hali yo'q bo'lsa — yaratadi
        username = os.environ.get('ADMIN_USERNAME')
        password = os.environ.get('ADMIN_PASSWORD')
        User = get_user_model()
        if username and password and not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(username=username, email='', password=password)
            self.stdout.write(f"Superuser '{username}' yaratildi")
