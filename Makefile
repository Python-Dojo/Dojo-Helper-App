test_all:
	python -m unittest discover -v

test_replit_scrapper:
	python -m unittest ./tests/test_replit_scrapper

test_github_archiver:
	python -m unittest ./tests/test_github_archiver

lint:
	flake8