echo "Running python manage.py collectstatic"
python manage.py collectstatic --noinput

echo "make migrate"
python manage.py migrate

echo "populating data"
python -m utils.populate

echo "Make log file"
if [ ! -d "run/logs" ]; then
 mkdir -p run/logs
fi

echo "Run uwsgi"
if [ ! -d "run" ]; then
  mkdir run && mkdir -p run/logs
fi

uwsgi -d --ini uwsgi.ini

echo "chmod api.sock"
chmod 777 run/api.sock
chmod +x run/api.sock

echo "Run celery"
celery multi start -A forum_backend_project worker -l info -c 1
echo "Await celery worker"
until timeout 30 celery -A forum_backend_project inspect ping; do >&2 echo "Celery workers not available"; done

echo "Starting flower"
celery -A forum_backend_project flower --address=0.0.0.0 --port=5555 --url_prefix=flower --loglevel=info --auto_refresh=True