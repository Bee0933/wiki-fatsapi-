install:
	# install dependencies
	pip install --upgrade pip &&\
		pip install -r requirements.txt 
format:
	# format python code with black
	black *.py logic/*.py api/*.py tests/*.py
lint:
	# check code syntaxes
	pylint --disable=R,C *.py logic/*.py api/*.py tests/*.py
test:
	# unit tests
	python3 -m pytest -vv --cov=api --cov=main tests/test_api.py
testdb:
	# test db
	python3 -m pytest -vv --cov=api --cov=main tests/test_db.py  

all: install format lint test testdb