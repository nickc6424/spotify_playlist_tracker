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
