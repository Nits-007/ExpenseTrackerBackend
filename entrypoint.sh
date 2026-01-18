#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
exec "$@"


# run setup tasks every time the container starts
# Runs database migrations
# Collects static files
# Starts the actual command passed to the container (e.g. gunicorn)

# Why NOT put this directly in the Dockerfile?
# 1️. Dockerfile runs at build time
#     Commands in a Dockerfile (RUN ...) execute once when the image is built, not when the container runs.
#     But:
#         DB may not be ready at build time
#         You may redeploy the same image multiple times
#         Migrations should run each time the container starts
# 2. Containers may restart
#     If:
#         The container crashes
#         Render / Railway / AWS restarts it
#         You scale replicas
#         You want migrations + static collection to run again safely