# telegram-seriea-bot
A Telegram bot that provides data and statistics about Serie A, the italian soccer league.

Data by https://api.football-data.org \
Powered by https://github.com/python-telegram-bot/python-telegram-bot

Contacts: andreamazzoni78@gmail.com

##Try @serieabot
If you want to play with my bot just add `@serieabot` to your telegram contacts
and fire some commands. 

This is a list of available commands:

- `ranking`: actual ranking
- `matchday`: results/scheduling
- `players`: team's players
- `player`: player details
- `help`: details about commands

##Run your own bot
In order to run the bot you have to provide:

- A Docker instance (https://docs.docker.com/install/)
- A Telegram bot token (https://core.telegram.org/bots#3-how-do-i-create-a-bot)

Then you have to build and run your container:
```bash
$ make docker-run TOKEN="<your token>"
```
Or if you want to run your bot in background mode:
```bash
$ make docker-deploy TOKEN="<your token>"
```