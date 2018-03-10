#Makefile
SHELL=/bin/bash

run:
	source env/bin/activate && \
	export BOT_TOKEN=$(TOKEN) && \
	export LOG_LEVEL=DEBUG && \
	export FOOTBALL_DATA_HOSTNAME=api.football-data.org && \
	export PROTOCOL=http && \
	python src/bot.py

docker-run:
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -i --rm \
	--env "BOT_TOKEN=$(TOKEN)" \
	--env "LOG_LEVEL=DEBUG" \
	--env "FOOTBALL_DATA_HOSTNAME=api.football-data.org" \
	--env "PROTOCOL=https" \
	--name telegram-seriea-bot \
	telegram-seriea-bot python src/bot.py

docker-deploy:
	-docker stop telegram-seriea-bot
	-docker rm telegram-seriea-bot
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -d \
	--env "BOT_TOKEN=$(TOKEN)" \
	--env "LOG_LEVEL=WARNING" \
	--env "FOOTBALL_DATA_HOSTNAME=api.football-data.org" \
	--env "PROTOCOL=http" \
	--name telegram-seriea-bot \
	telegram-seriea-bot python src/bot.py
