# Oneworksite pythonanywhere notes

## SSH access

`ssh sniffers@ssh.pythonanywhere.com`

public keys installed in `~/.ssh/authorized_keys`

### pythonanywhere pubkey

This should be added to any repo's read-only access for deployment.

`.ssh/id_rsa.pub`:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDKdfSVi39QJjezb8W+PU3c5Sa2BYww7jhTjDdr2lWrL7MtX9S8Brf+CqxPB6Ao8g4fAMbcN/m5O0cs/B7iKXl2A+qWD6ELXmAz4EeyuO32wC7PTvH8knryEIL8iwWh7paL9DXRAX00jKjPi8wySAxpWDQaPKokmSGBG/MHL2AFQkTEY5JaUTeZmqMpOPA48nEejHgOJvjlqZXAnvvg07A1HGNsclBhORIOTFmUjDj+E6Nr452hEy++dYRpRKT1yseativyXNwdAjIKx4CQFGS3hkkCg418StI/nZt3DV94WY/HNuPEr9nO3IHkdC663h81HBfRTW5HXACJNP2FVtc/ sniffers@giles-liveconsole1
```

## Instances

When working with `manage.py`, use following:

`DJANGO_SETTINGS_MODULE='config.settings.live' python manage.py ...`

### `sniffers.pythonanywhere.com` - test

* venv: `/home/sniffers/.virtualenvs/snifferstest/`
* repo: `/home/sniffers/repos/snifferstest/`
* db: `sniffers$snifferstest`

### `sniffers.oneworksite.com` - prod

* venv: `/home/sniffers/.virtualenvs/sniffersprod/`
* repo: `/home/sniffers/repos/sniffersprod/`
* db: `sniffers$sniffersprod`

## Databases

* Host: `sniffers.mysql.pythonanywhere-services.com`
* Username: `sniffers`
* Password: `CorcAcFegIgshy7`
* Database names start with `sniffers$<name>` (see above section)

## Email via Mailgun

* SMTP hostname: `smtp.mailgun.org`
* Username: `postmaster@mg.oneworksite.com`
* Password: `d47b712836d312d101f05947e5c5be9d-b892f62e-1500b698`

## Setup instructions for new instance

Useful links:

* https://www.miniwebtool.com/django-secret-key-generator/

### venv & django

1. `mkvirtualenv $NAME --python=/usr/bin/python3.6`
2. Clone repo to `~/repos/$REPONAME` (call this `$REPO`) and `cd $REPO`
3. `pip install -U pip setuptools`
4. `pip install pymysql -r $REPO/requirements.txt`
5. Create new database on pythonanywhere
6. Create a file named `$REPO/config/settings/live.py` and populate it as follows:

       import os
       os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.live'
       os.environ['DJANGO_SECRET_KEY'] = '$SECRET_KEY_HERE'
       os.environ['DJANGO_ALLOWED_HOSTS'] = '$HOSTNAME'
       os.environ['DJANGO_DATABASE_URL'] = 'mysql://sniffers:$DBPASS@sniffers.mysql.pythonanywhere-services.com/$DBNAME'

       from .pythonanywhere import *

7. `export DJANGO_SETTINGS_MODULE='config.settings.live'`
8. `python manage.py migrate`
9. `python manage.py collectstatic`
10. `python manage.py createsuperuser`
11. `ln -s /var/www/$DOMAIN_wsgi.py $REPO/wsgi.py`

### pythonanywhere config

1. Create new webapp - custom, python 3.6
2. Set source code to `$REPO` - sometimes this needs to be done multiple times to stick
3. Set working directory and virtualenv to `/home/sniffers/.virtualenvs/$NAME` -- **DO NOT just use `$NAME` as it doesn't work**
4. Add static file mapping:

       /static/ -> $REPO/staticfiles

5. Open wsgi file and paste the following:

       from config.settings.live import *

       from django.core.wsgi import get_wsgi_application
       application = get_wsgi_application()

6. Reload app and test.
7. Profit!

## Deployment

A git `post-receive` hook will automatically call the `scripts/deploy.sh` script in the
test instance. This **will not** happen automatically in production.

### Manual deployment

ssh to instance and run either:

* `DEPLOY_NAME=sniffersprod ~/deploy.sh` or
* `DEPLOY_NAME=snifferstest ~/deploy.sh`
