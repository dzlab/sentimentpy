#!/bin/sh
# this script will setup the enviroment by installing prerequisites

echo "Installing python dev tools"
sudo apt-get install python-pip python-dev build-essential
sudo apt-get install python3 python3-pip
sudo pip install virtualenv
virtuanenv DEV
source DEV/bin/activate

echo "Installing python libraries in current virtualenv"
pip install nose
pip install numpy 
sudo apt-get install libatlas-base-dev gfortran
pip install scipy
pip install python-dateutil

echo "Installing python libraries for webapp"
pip install Flask
pip install flask-wtf

echo "Installing language detection libraries"
pip install pyenchant
pip install --pre guess_language-spirit

echo "Installing language dictionaries"
sudo apt-get install -y hunspell-en-us hunspell-ru hunspell-de-de hunspell-fr hunspell-eu-es

echo "Installing mongodb"
mkdir -p ~/Data/mongodb
mkdir -p ~/Programs
cd ~/Programs/
wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.4.tgz
tar xvf mongodb-linux-x86_64-2.6.4.tgz
rm mongodb-linux-x86_64-2.6.4.tgz

echo "launching mongodb daemon"
cd mongodb-linux-x86_64-2.6.4/bin
./mongod --dbpath ~/Data/mongodb
