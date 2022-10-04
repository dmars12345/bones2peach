#!/bin/bash
sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
sudo apt install needrestart
sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf
git clone GITURL
mv /root/bones2peaches/bash/terraform.sh /root/terraform.sh
sudo chmod +x terraform.sh
sh terraform.sh
mv /root/bones2peaches/bash/aws.sh /root/aws.sh
sudo chmod +x aws.sh
sh aws.sh
mv /root/bones2peaches/bash/buckets.sh /root/buckets.sh
sudo chmod +x buckets.sh
sh buckets.sh
mv /root/bones2peaches/bash/roles.sh /root/roles.sh
sudo chmod +x roles.sh
sh roles.sh
mv /root/bones2peaches/bash/docker.sh /root/docker.sh
sudo chmod +x docker.sh
sh docker.sh
mv /root/bones2peaches/bash/cron.sh /root/cron.sh
sudo chmod +x cron.sh
sh cron.sh
cd /root/bones2peaches/tf
python3 aws.py
cd /root/bones2peaches/v4/extract
python3 v4_extract.py







