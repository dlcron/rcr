app:
	docker compose run --service-ports app

build:
	docker compose build

test:
	docker compose run dev pytest --pdb

lint:
	docker compose run dev /bin/sh -c 'mypy . && ruff check . --fix'


.PHONY: app build test lint
