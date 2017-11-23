
# lolbot dockerfile
# licensed under MIT License
# (c) 2017 S Stewart
FROM alpine:3.6

MAINTAINER "S Stewart <iamtheworst@programmer.net>"

# make dir
RUN mkdir /opt/lolbot
# do shit
WORKDIR /opt/lolbot
# install reqs
RUN apk add --no-cache python3
COPY requirements.txt /opt/lolbot
RUN pip install -r requirements.txt

# add real source
COPY . /opt/lolbot

# run!!!
CMD ["python", "/opt/lolbot/index.py"]
