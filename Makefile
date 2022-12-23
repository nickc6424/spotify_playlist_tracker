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
# 			 Testing 
#--------------------------------

linting-test: ## run linting checks
	$(VENV_DIR)/bin/python -m black --check --diff --line-length 120 .

unit-test: ## run unit tests
	PYTHONPATH=. $(VENV_DIR)/bin/python -m pytest

test: linting-test unit-test ## run all tests
