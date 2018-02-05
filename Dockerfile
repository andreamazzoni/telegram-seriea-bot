FROM python:latest

#Adjust timezone
RUN ln -fs /usr/share/zoneinfo/Europe/Rome /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

#install libraries
RUN pip install pipenv
RUN pip install python-telegram-bot

#copy bot files
COPY ["src/*","src/"]

CMD ["python","src/bot.py"]