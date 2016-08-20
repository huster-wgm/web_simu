web: gunicorn simu_tool.wsgi --log-file -
web: python simu_tool/manage.py collectstatic --noinput;
bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT simu_tool/settings.py