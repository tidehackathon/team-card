PYTHON=./.venv/bin/python
PIP=./.venv/bin/pip

create-virtualenv: 
	python3 -m venv .venv
	${PIP} install --upgrade pip
	${PIP} install -r requirements.txt 

run-tests:
	${PYTHON} -m pytest 

setup-local-api:
	uvicorn src.model_api.api:app --reload