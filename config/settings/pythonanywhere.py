"""
Pythonanywhere settings
This pulls in settings from the environment, probably `conf/settings/live.py`
"""

from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

DATABASES['default'] = env.db('DJANGO_DATABASE_URL')
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

# Set mysql strict mode
# http://django-mysql.readthedocs.io/en/latest/checks.html#django-mysql-w001-strict-mode
# https://docs.djangoproject.com/en/2.0/ref/databases/#mysql-sql-mode
if 'mysql' in DATABASES['default']['ENGINE']:
    if not 'OPTIONS' in DATABASES['default']:
        DATABASES['default']['OPTIONS'] = {}
    DATABASES['default']['OPTIONS']['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES'"
