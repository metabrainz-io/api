#!/bin/bash

apt-get update -y && \
apt-get -y install openssh-server dos2unix build-essential && \
apt-get -y install python3-dev python3-pip python3-venv && \
apt-get -y install net-tools nginx sudo git nano