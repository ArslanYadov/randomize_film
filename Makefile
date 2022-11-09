VENV=venv
MANAGE_PATH='./randomize_film'

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help: ## вывод доступных команд
	@echo 'Список доступных команд.'
	@echo ''
	$(call find.functions)
setup: ## установить и запустить консольное приложение
setup: venv pipin init run

venv: ## установка и активация виртуального окружения
venv:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate

pipin: ## установка/обновление pip
pipin:
	pip install -U pip

init: ## установка зависимостей из requirements.txt
init:
	pip install -r requirements.txt

run: ## запустить консольное приложение
run: 
	cd $(MANAGE_PATH); python3 random_film.py

clean: ## очистка кэша
clean:
	cd $(MANAGE_PATH); rm -rf __pycache__
