#Makefile
SHELL=/bin/bash

local-run:
	export FLASK_APP=bot_server.py
	flask run

aws-deploy:
	zappa update $(env)
