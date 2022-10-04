import boto3

import json
ec2_resource = boto3.resource('ec2',aws_access_key_id='ACCESS',
aws_secret_access_key='SECRET',region_name = 'us-east-1')

role = 'arn:aws:iam::AWSID:instance-profile/AmazonSSMRoleForInstancesQuickSetup'

sg  = {'vpc': 'vpc-006b9173fa9abbb97', 'id': 'sg-07451250d618ed197'


USERDATA_SCRIPT = '''#!/bin/bash
sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
sudo apt install needrestart
sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf
git clone "GITCLONEURL"
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
python3 v4_extract.py'''


api_instance= ec2_resource.create_instances(
        ImageId="ami-052efd3df9dad4825",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        UserData = USERDATA_SCRIPT,
        KeyName="stalk",
    SecurityGroupIds = [sg['id']]
    )

instance_id = str(api_instance).split('-')[1].replace("')","").replace(']',"")
