requirements:
	bash -c 'source venv/bin/activate; pip freeze > requirements.txt;'

install:
	docker-compose -p pikabase -f docker/docker-compose.yml build
	docker-compose -p pikabase -f docker/docker-compose.yml up -d

install_pikabase_app:
	docker-compose -p pikabase -f docker/docker-compose.yml build pikabase-app
	docker-compose -p pikabase -f docker/docker-compose.yml up -d pikabase-app

install_pikabase_db:
	docker-compose -p pikabase -f docker/docker-compose.yml build pikabase-db
	docker-compose -p pikabase -f docker/docker-compose.yml up -d pikabase-db

destroy_data:
	x-terminal-emulator -e "sudo rm -Rf data"

down:
	docker-compose -p pikabase -f docker/docker-compose.yml down

delete: down destroy_data

migrate:
	docker exec -it pikabase-app python manage.py migrate
