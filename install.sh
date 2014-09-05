#!/bin/sh

echo "Installing mongodb"
mkdir -p ~/Data/mongodb
mkdir -p ~/Programs
cd ~/Programs/
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.4.tgz
tar xvf mongodb-linux-x86_64-2.6.4.tgz
rm mongodb-linux-x86_64-2.6.4.tgz

echo "launching mongodb daemon"
cd mongodb-linux-x86_64-2.6.4/bin
./mongod --dbpath ~/Data/mongodb
