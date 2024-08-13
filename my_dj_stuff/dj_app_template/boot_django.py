# File sets up the django environment, used by other scripts that need to
# execute in Django land
import sys
from pathlib import Path
import django
from django.conf import settings

BASE_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(BASE_DIR))   # adds the "src" path to python's path, so Python can find it


def boot_django():
    """set up of django environment. Same settings as in settings.py of a project
    """
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default":{
                "ENGINE":"django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        },
        INSTALLED_APPS=(
            "dj_app1",
        ),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()