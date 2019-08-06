web: gunicorn mailing.wsgi
main_worker: celery --app=celery.app worker --beat --loglevel=info