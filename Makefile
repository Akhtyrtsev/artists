clean:
	sudo bash clean_containers.sh

build:
	sudo docker-compose -f docker-compose-local.yml build

run:
	sudo docker-compose -f docker-compose-local.yml up -d

down:
	sudo docker-compose -f docker-compose-local.yml down

django-logs:
	sudo docker-compose -f docker-compose-local.yml logs -f backend

celery-logs:
	sudo docker-compose -f docker-compose-local.yml logs -f celery

celery-beat-logs:
	sudo docker-compose -f docker-compose-local.yml logs -f celery-beat

makemigrations:
	sudo docker exec -it artists_backend python manage.py makemigrations

migrate:
	sudo docker exec -it artists_backend python manage.py migrate

shell:
	sudo docker exec -it artists_backend python manage.py shell

test:
	sudo docker exec -it artists_backend python manage.py test api.tests --settings=artists.settings.testing




