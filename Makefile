build:
./build.sh

render-start:
gunicorn task_manager.wsgi

install:
uv sync

collectstatic:
uv run python manage.py collectstatic --noinput

migrate:
uv run python manage.py migrate
