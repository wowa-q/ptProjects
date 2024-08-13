from django.core.management import call_command
from my_dj_stuff.dj_app_template.boot_django import boot_django

boot_django()
# python manage.py makemigrations can be done with this call:
call_command("makemigrations", "dj_app1")