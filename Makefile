CODE_FOLDERS := src db

PHONY: docker_run install run format lint test
docker_run:
	docker-compose up

install:
	poetry install

run:
	uvicorn main:app

format:
	poetry run black --line-length 79 --skip-string-normalization $(CODE_FOLDERS) $(TEST_FOLDERS)

lint:
	poetry run flake8 --extend-ignore W291 src

test:
	poetry run pytest

run_bandit:
	poetry run bandit -r src/ -f csv -o out.csv