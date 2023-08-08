#!/bin/bash

# Update the system
sudo apt-get update -y

# Install dependencies
sudo apt-get install -y curl gnupg debian-keyring debian-archive-keyring apt-transport-https

# Add RabbitMQ signing key
curl -1sLf 'https://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc' | sudo apt-key add -

# Add Erlang Solutions repository
echo "deb https://packages.erlang-solutions.com/ubuntu focal contrib" | sudo tee /etc/apt/sources.list.d/erlang.list

# Update the package database
sudo apt-get update -y

# Install Erlang
sudo apt-get install -y esl-erlang

# Add RabbitMQ repository
echo "deb https://dl.bintray.com/rabbitmq/debian focal main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list

# Update the package database
sudo apt-get update -y

# Install RabbitMQ
sudo apt-get install -y rabbitmq-server

# Enable and start the RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# Check the status of RabbitMQ
sudo systemctl status rabbitmq-server

echo "RabbitMQ installation completed!"
