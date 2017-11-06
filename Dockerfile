
# lolbot dockerfile
# licensed under MIT License
# (c) 2017 S Stewart
FROM python:3

MAINTAINER "S Stewart <iamtheworst@programmer.net>"

# make dir
RUN mkdir /opt/lolbot
# do shit
WORKDIR /opt/lolbot
# install reqs
COPY requirements.txt /opt/lolbot
RUN pip install -r requirements.txt

# add real source
COPY . /opt/lolbot

# run!!!
CMD ["python", "/opt/lolbot/index.py"]
