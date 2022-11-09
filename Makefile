VENV=venv
MANAGE_PATH='./randomize_film'

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help: ## вывод доступных команд
	@echo 'Список доступных команд.'
	@echo ''
	$(call find.functions)
setup: ## установить консольное приложение
setup: venv pipin init

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

rvenv: ## очистка виртуального окружения
rvenv:
	rm -rf $(VENV)

clean: ## очистка кэша
clean:
	cd $(MANAGE_PATH); rm -rf __pycache__

leave: ## удалить виртуальное окружение и очистить кэш
leave: rvenv clean
