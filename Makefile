test_all:
	python -m unittest discover -v

test_replit_scrapper:
	python -m unittest ./tests/test_replit_scrapper.py

test_github_archiver:
	python -m unittest ./tests/test_github_archiver.py

lint:
	flake8