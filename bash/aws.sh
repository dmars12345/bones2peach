#!/bin/bash
sudo apt install zip -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip -y
sudo ./aws/install
aws --profile default configure set aws_access_key_id "ACCESS"
aws --profile default configure set aws_secret_access_key "SECRET"
aws --profile default configure set region "us-east-1"
