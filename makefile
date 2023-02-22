PYTHON=./.venv/bin/python
PIP=./.venv/bin/pip

create-virtualenv: 
	python3 -m venv .venv
	${PIP} install --upgrade pip
	${PIP} install -r requirements.txt 

run-tests:
	${PYTHON} -m pytest 

score-dl-model:
	${PYTHON} -i -m src.scoring_dl_models.score

