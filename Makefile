#Makefile
SHELL=/bin/bash

run:
	source env/bin/activate && \
	export BOT_TOKEN=$(BOT_TOKEN) && \
	export FOOTBALL_DATA_TOKEN=$(FD_TOKEN) && \
	export FOOTBALL_DATA_HOSTNAME=api.football-data.org && \
	export FOOTBALL_DATA_PROTOCOL=https && \
	export LOG_LEVEL=DEBUG && \
	python src/bot.py

docker-run:
	-docker stop telegram-seriea-bot
	-docker rm telegram-seriea-bot
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -i --rm \
	--env "BOT_TOKEN=$(BOT_TOKEN)" \
	--env "LOG_LEVEL=DEBUG" \
	--env "FOOTBALL_DATA_TOKEN=$(FOOTBALL_DATA_TOKEN)" \
	--env "FOOTBALL_DATA_HOSTNAME=api.football-data.org" \
	--env "FOOTBALL_DATA_PROTOCOL=https" \
	--name telegram-seriea-bot \
	telegram-seriea-bot python src/bot.py

docker-deploy:
	-docker stop telegram-seriea-bot
	-docker rm telegram-seriea-bot
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -d \
	--env "BOT_TOKEN=$(BOT_TOKEN)" \
	--env "LOG_LEVEL=WARNING" \
	--env "FOOTBALL_DATA_TOKEN=$(FOOTBALL_DATA_TOKEN)" \
	--env "FOOTBALL_DATA_HOSTNAME=api.football-data.org" \
	--env "FOOTBALL_DATA_PROTOCOL=https" \
	--name telegram-seriea-bot \
	telegram-seriea-bot python src/bot.py
