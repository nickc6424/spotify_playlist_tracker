VENV_DIR=./venv

# -------------------------------
# 	Virtual environment setup 
#--------------------------------

install-requirements: ## Installs packages from requirements file
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r ./requirements.txt

create-venv: ## create a local virtual environment for python
	python3 -m venv "$(VENV_DIR)"

venv: create-venv install-requirements ## Create virtual environment + install packages


# -------------------------------
# 			 Docker 
#--------------------------------

start:
	sudo docker compose up local-s3 --detach
	sudo docker compose up postgres --detach

stop:
	sudo docker compose down --volumes

s3-read: ## View the files in the S3 bucket
	aws s3 ls s3://playlist-extracts --endpoint-url=http://localhost:4566 --recursive

s3-drop: ## Drop the S3 bucket
	aws s3 rb s3://playlist-extracts --endpoint-url=http://localhost:4566 --force

s3-dl: ## Download files from the S3 bucket
	aws s3 cp s3://playlist-extracts ./s3_download/ --endpoint-url=http://localhost:4566 --recursive

db-read: ## Read from the database table
	docker exec -it spotify_playist_tracker-postgres-1 psql -c 'SELECT * FROM spotify.import.tbl_playlist_snapshot LIMIT 100;' -U spotify

db-drop: ## Drop the database table
	docker exec -it spotify_playist_tracker-postgres-1 psql -c 'DROP TABLE IF EXISTS spotify.import.tbl_playlist_snapshot;' -U spotify
	docker exec -it spotify_playist_tracker-postgres-1 psql -c 'DROP SCHEMA IF EXISTS import;' -U spotify

reset: s3-drop db-drop

# -------------------------------
# 			 Testing 
#--------------------------------

linting-test: ## run linting checks
	$(VENV_DIR)/bin/python -m black --check --diff --line-length 120 .

unit-test: ## run unit tests
	PYTHONPATH=./scripts $(VENV_DIR)/bin/python -m pytest

test: linting-test unit-test ## run all tests
