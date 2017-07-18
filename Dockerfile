
# lolbot dockerfile
# licensed under MIT License
# (c) 2017 S Stewart

# define the image used (in this case - it's python.)
FROM python:3
# obvs I need credit inside the file
MAINTAINER "S Stewart <iamtheworst@programmer.net>"
RUN echo "We are going to start in a few seconds."
RUN echo "Please make sure your config.json is setup"
RUN sleep 3
# The moment you've been waiting for... actually installing lolbot
VOLUME ["/srv/lolbot"]
WORKDIR /srv/lolbot
RUN pip install -Ur requirements.txt
# and we're gonna run it!
CMD ["python", "/srv/lolbot/index.py"]
