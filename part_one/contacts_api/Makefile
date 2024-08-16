.PHONY: setup-env dev deploy

setup-env:
	cp .env-example .env

dev: setup-env
	docker-compose up --build

deploy: setup-env
	docker-compose up --build -d
