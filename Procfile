web: gunicorn mailing.wsgi
main_worker: celery -A mailing worker --beat --loglevel=info