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
	python3 -m pytest -vv --cov=api --cov=main tests/test_db.py
build:
	# build docker container
	docker build -t deploy-wiki .
run:
	# run docker
	# docker run -p 127.0.0.1:8001:8001 b94c425346ee
deploy:
	# deploy application
	
all: install format lint test build 