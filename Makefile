install:
	pip install -r requirements.txt

test:
	coverage run -m unittest discover sunflower/tests -v
