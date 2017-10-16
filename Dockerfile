
# lolbot dockerfile
# licensed under MIT License
# (c) 2017 S Stewart
FROM python:3

# make dir
RUN mkdir /opt/lolbot
# do shit
WORKDIR /opt/lolbot
# install reqs
ADD requirements.txt /opt/lolbot
RUN pip install -r requirements.txt

# add real source
ADD . /opt/lolbot

# run!!!
CMD ["python", "/opt/lolbot/index.py"]