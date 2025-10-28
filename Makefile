build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

install:
	uv sync

setup:
	uv sync
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

lint:
	uv run ruff check

test:
	uv run python manage.py test

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py migrate --noinput