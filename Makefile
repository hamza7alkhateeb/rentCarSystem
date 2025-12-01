# ---- DOCKER ----

build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

restart:
	docker-compose down && docker-compose up -d

shell:
	docker-compose exec web bash


# ---- DJANGO ----

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser


# ---- CELERY ----

celery-logs:
	docker-compose logs -f celery_worker

celery-beat-logs:
	docker-compose logs -f celery_beat
