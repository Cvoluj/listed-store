MANAGE_PY_FILE = listedStore/manage.py


.PHONY: runserver
runserver:
	python ${MANAGE_PY_FILE} runserver

.PHONY: makemigrations
makemigrations:
	python ${MANAGE_PY_FILE} makemigrations

.PHONY: migrate
migrate:
	python ${MANAGE_PY_FILE} migrate


.PHONY: runreact
runreact:
	npm run start

.PHONY: generate_fernet
generate_fernet:
	python listedStore/listedStore/generate_fernet_key.py
