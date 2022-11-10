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
	aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 531338205655.dkr.ecr.us-east-2.amazonaws.com
	docker build -t wiki-fast .
	docker tag wiki-fast:latest 531338205655.dkr.ecr.us-east-2.amazonaws.com/wiki-fast:latest
	docker push 531338205655.dkr.ecr.us-east-2.amazonaws.com/wiki-fast:latest

all: install format lint test deploy 