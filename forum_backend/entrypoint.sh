echo "Running python manage.py collectstatic"
python manage.py collectstatic --noinput

echo "make migrate"
python manage.py migrate

echo "populating data"
python -m utils.populate


echo "Run uwsgi"
uwsgi -d --ini uwsgi.ini
echo "Run celery"
celery multi start -A forum_backend_project worker -l info -c 1
echo "Await celery worker"
until timeout 10 celery -A forum_backend_project inspect ping; do >&2 echo "Celery workers not available"; done

echo "Starting flower"
celery -A forum_backend_project flower --address=0.0.0.0 --port=5555 --url_prefix=flower --loglevel=info --auto_refresh=True