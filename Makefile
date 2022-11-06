install:
	# install dependencies
	pip install --upgrade pip &&\
		pip install -r requirements.txt 
format:
	# format python code with black
	black *.py logic/*.py test/*.py api/*.py
lint:
	# check code syntaxes
	pylint --disable=R,C *.py logic/*.py test/*.py api/*.py
test:
	# unit tests