#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
sudo apt-get install -y git
sudo apt-get update -y
sudo apt-get install -y python-dev
sudo apt-get install -y python-pip
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update -y
sudo apt-get install -y mongodb-org
sudo service mongod start
echo "Cloning package from github"
sudo git clone "https://github.com/liyefei737/CSC326"
sudo chmod -R 777 CSC326/
cd CSC326

sudo apt-get install python-beautifulsoup
sudo pip install numpy
sudo pip install pymongo
sudo pip install oauth2client
sudo pip install google-api-python-client
sudo pip install bottle==0.12.13
sudo pip install beaker

sudo python crawler.py
nohup sudo python frontend.py