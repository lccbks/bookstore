FROM ubuntu:20.04
MAINTAINER yxlee777 yxleezw@163.com
LABEL description="docker image for bookstore"
# ADD sources.list /etc/apt/
COPY . /home/bookstore
WORKDIR /home/bookstore

RUN apt-get update \
	&& apt-get install -y python3 python3-pip \
	&& pip3 install -r /home/bookstore/requirements.txt \
	&& apt-get install -y curl \
	&& apt-get install -y mysql-server \
	&& service mysql start \
	&& mysql -u root < /home/bookstore/create_user.sql \
	&& mysql -u bookstore -pBookstore@2020 < /home/bookstore/bookstore.sql

EXPOSE 5000

CMD export PYTHONPATH=$PYTHONPATH:$(pwd) \
	&& service mysql start \
	&& /bin/bash
