#!/bin/bash
mv /root/bones2peaches/resources/ecrrole.json /root/ecrrole.json
sudo apt-get remove docker docker-engine docker.io
sudo apt-get update
sudo apt install docker.io -y
sudo snap install docker
docker login -u DOCKERUSER -p DOCKERPASS
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWSID.dkr.ecr.us-east-1.amazonaws.com
aws ecr create-repository --repository-name v4-log-pipeline2 --image-scanning-configuration scanOnPush=true --region us-east-1
aws ecr set-repository-policy --repository-name v4-log-pipeline2 --policy-text file://ecrrole.json
mkdir app
mv /root/bones2peaches/v4/load/ids /root/app/
cd app
mkdir app
mv /root/app/ids/series/series.py /root/app/app/main.py
mv /root/app/ids/series/Dockerfile /root/app/app/Dockerfile
mv /root/app/ids/series/crontab /root/app/app/crontab
cd app
docker build -t series1:fw_series1 .
docker run -d series1:fw_series1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWSID.dkr.ecr.us-east-1.amazonaws.com
docker tag series1:fw_series1 AWSID.dkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_series1
docker push AWSID.dkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_series1
rm main.py
mv /root/app/ids/site_sections/site_sections.py /root/app/app/main.py
docker build -t site_sections:fw_site_sections .
docker run -d site_sections:fw_site_sections
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWSID.dkr.ecr.us-east-1.amazonaws.com
docker tag site_sections:fw_site_sections AWSID.dkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_site_sections
docker push AWSID.dkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_site_sections
rm main.py
mv /root/app/ids/sites/sites.py /root/app/app/main.py
docker build -t sites:fw_sites .
docker run -d sites:fw_sites
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin AWSID.dkr.ecr.us-east-1.amazonaws.com
docker tag sites:fw_sites AWSID.dkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_sites
docker push AWSIDdkr.ecr.us-east-1.amazonaws.com/v4-log-pipeline2:fw_sites
