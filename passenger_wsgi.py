# cPanel "Setup Python App" (Phusion Passenger) uchun kirish nuqtasi
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teplo.settings')

from teplo.wsgi import application  # noqa: E402,F401
