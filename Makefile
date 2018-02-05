build:
	docker build -t telegram-seriea-bot .
	docker image prune -f

run-test:
	#capolista_bot
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -it --rm \
	--env "BOT_TOKEN=<token>" \
	--env "LOG_LEVEL=DEBUG" \
	--env "FOOTBALL_DATA_HOSTNAME=https://api.football-data.org" \
	--name telegram-seriea-bot \
	telegram-seriea-bot


deploy:
	#serieabot
	-docker stop telegram-seriea-bot
	-docker rm telegram-seriea-bot
	docker build -t telegram-seriea-bot .
	docker image prune -f
	docker run -d \
	--env "BOT_TOKEN=<token>" \
	--env "LOG_LEVEL=WARNING" \
	--env "FOOTBALL_DATA_HOSTNAME=https://api.football-data.org" \
	--name telegram-seriea-bot \
	telegram-seriea-bot