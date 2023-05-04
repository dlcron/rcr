test:
	docker compose run dev pytest --pdb

app:
	docker compose run --service-ports app

.PHONY: test app
