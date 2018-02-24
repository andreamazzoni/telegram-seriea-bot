FROM python:latest

#Adjust timezone
RUN ln -fs /usr/share/zoneinfo/Europe/Rome /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

SHELL ["/bin/bash", "-c"]

#copy source files and dependencies
COPY . /telegram-seriea-bot/
WORKDIR /telegram-seriea-bot
RUN pip install virtualenv && \
    virtualenv env && \
    source env/bin/activate && \
    pip install -r requirements.txt

ENTRYPOINT ["/telegram-seriea-bot/entrypoint.sh"]
