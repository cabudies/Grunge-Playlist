.PHONY: lint format test testfast ready dumpinitialdata

format:
	isort --atomic --skip-glob="venv/*" grunge
	black --exclude="venv/" grunge

lint:
	flake8 grunge
	black --check --exclude="venv/" grunge

test:
	python manage.py test

testfast:
	python manage.py test --failfast

ready: lint testfast

dumpinitialdata:
	python manage.py dumpdata --natural-foreign --natural-primary \
		--exclude=admin.logentry --all --indent=2 > grunge/fixtures/initial_data.json
