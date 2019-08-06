web: gunicorn mailing.wsgi
main_worker: celery --app=mailing.celery worker --beat --loglevel=info