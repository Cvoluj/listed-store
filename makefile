MANAGE_PY_FILE = listedStore/manage.py
FRONTEND = frontend/


.PHONY: runserver
runserver:
	python ${MANAGE_PY_FILE} runserver


.PHONY: runreact
runreact:
	npm --prefix FRONTEND run start
