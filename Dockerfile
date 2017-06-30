# lolbot dockerfile
# licensed under MIT License
# (c) 2017 S Stewart

# define the image used (in this case - it's ubuntu.)
FROM ubuntu
# obvs I need credit inside the file
MAINTAINER "S Stewart <iamtheworst@programmer.net>"
# do a quick update first to make sure everything's up to date
RUN apt update
RUN apt upgrade -y
# Run the mkdir to make some place for it
RUN mkdir /srv
# Install deps
RUN apt install python3.6 wget screen -y
# deps part 2 - pip
RUN cd /tmp
RUN wget -O pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3.6 pip.py
RUN rm pip.py
# The moment you've been waiting for... actually installing lolbot
RUN cd /srv
VOLUME ["/srv/lolbot"]
RUN cd lolbot
RUN pip3.6 install -Ur requirements.txt
# and we're gonna run it!
CMD ["-dm /srv/lolbot/index.py"]
ENTRYPOINT usr/bin/screen
