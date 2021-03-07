requirements:
	bash -c 'source venv/bin/activate; pip freeze > requirements.txt;'

install: up sleep_10_sec migrate

up:
	docker-compose -p pikabase -f docker/docker-compose.yml build
	docker-compose -p pikabase -f docker/docker-compose.yml up -d

up_pikabase_app:
	docker-compose -p pikabase -f docker/docker-compose.yml build pikabase-app
	docker-compose -p pikabase -f docker/docker-compose.yml up -d pikabase-app

up_pikabase_db:
	docker-compose -p pikabase -f docker/docker-compose.yml up -d pikabase-db

up_rabbitmq:
	docker-compose -p pikabase -f docker/docker-compose.yml up -d rabbitmq

migrate:
	docker exec -it pikabase-app python manage.py migrate

makemigrations:
	bash -c 'source venv/bin/activate; for i in $$(cat secrets/pikabase-app.env); do export $$i; done; python manage.py makemigrations'

restart_pikabase_app:
	docker-compose -p pikabase -f docker/docker-compose.yml restart pikabase-app

delete: down destroy_data

down:
	docker-compose -p pikabase -f docker/docker-compose.yml down

destroy_data:
	x-terminal-emulator -e "sudo rm -Rf data"

docker_hoster_run:
	docker run --rm -d --name docker-hoster -v /var/run/docker.sock:/tmp/docker.sock -v /etc/hosts:/tmp/hosts dvdarias/docker-hoster

docker_hoster_stop:
	docker stop docker-hoster

sleep_10_sec:
	sleep 10
