MANAGE_PATH='./randomize_film'

define find.functions
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
endef

help: ## вывод доступных команд
	@echo 'Список доступных команд.'
	@echo ''
	$(call find.functions)
start: ## запустить консольное приложение
start: 
	cd $(MANAGE_PATH); python3 random_film.py
