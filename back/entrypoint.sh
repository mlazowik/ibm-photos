#!/usr/bin/ash

python manage.py migrate

# XXX: Hacky as hell. Hardcoded password. Even if it wasn't this code wouldn't
# change the password of an previously created admin.
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', '(nG<s]uv{082z(')" | python manage.py shell

exec uwsgi --ini /opt/back/uwsgi.ini
