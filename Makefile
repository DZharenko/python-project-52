# build:
# 	./build.sh

# render-start:
# 	gunicorn task_manager.wsgi

# install:
# 	uv sync

# setup:
# 	uv sync
# 	uv run python manage.py migrate

# collectstatic:
# 	uv run python manage.py collectstatic --noinput

# migrate:
# 	uv run python manage.py migrate

# lint:
# 	uv run ruff check

# test:
# 	uv run python manage.py test

# ci-install:
# 	uv sync --group dev

# ci-migrate:
# 	uv run python manage.py migrate --noinput

install:
	uv sync

dev-install:
	uv sync --group dev

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

run:
	uv run python manage.py runserver

render-start:
	uv run gunicorn task_manager.wsgi

build:
	./build.sh

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

test:
	uv run pytest --ds=task_manager.settings --reuse-db

coverage:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=task_manager.settings
	uv run coverage report --show-missing --skip-covered

ci-install:
	uv sync --group dev

ci-migrate:
	uv run python manage.py makemigrations --noinput && \
	uv run python manage.py migrate --noinput

ci-test:
	uv run coverage run --omit='*/migrations/*,*/settings.py,*/venv/*,*/.venv/*' -m pytest --ds=task_manager.settings --reuse-db
	uv run coverage xml
	uv run coverage report --show-missing --skip-covered

locale:
	django-admin compilemessages --locale=ru

translate:
	django-admin makemessages -l ru -i venv