web: gunicorn mailing.wsgi
main_worker: celery worker --app=celery.app --beat --loglevel=info