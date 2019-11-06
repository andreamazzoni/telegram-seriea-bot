# telegram-seriea-bot
A Telegram bot that provides data and statistics about Serie A, the italian soccer league.

Data by https://api.football-data.org \
Powered by https://github.com/python-telegram-bot/python-telegram-bot

Contacts: andreamazzoni78@gmail.com

## Try @serieabot
If you want to play with my bot just add `@serieabot` to your telegram contacts
and fire some commands. 

This is a list of available commands:

- `ranking`: actual ranking
- `matchday`: results/scheduling
- `players`: team's players
- `player`: player details
- `scorers`: actual scorers ranking
- `help`: details about commands

## Run your own bot
In order to run the bot you have to provide:

- A Telegram bot token (https://core.telegram.org/bots#3-how-do-i-create-a-bot)
- A football-data token (https://api.football-data.org/client/register)

Put your tokens into `config.py` file and choose where to deploy your bot instance. There are some preconfigured options on makefile:

- `local-run` to launch a simple flask app locally
- `aws-deploy` to use zappa to deploy a lambda function on your configured AWS account (check `zappa_settings.json`)

Whatever your choice was then you will have to set a webhook on your telegram bot (https://core.telegram.org/bots/api#setwebhook)

Have fun!