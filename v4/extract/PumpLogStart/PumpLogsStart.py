import sys
import os
import json
from pathlib import Path
import boto3
import datetime as datetime
from datetime import date

auth = str('/root/loguserkey.json')


with open(auth,'r') as fp:
    creds = json.load(fp)

my_s3_resource =boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
my_s3_client =boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
today = str(datetime.date.today())
extracted_logs_paginator = my_s3_client.get_paginator('list_objects_v2')
extract_pages = extracted_logs_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix='extract/'+ str(datetime.date.today())+'/',)
extract_logs = []
for page in extract_pages:
    for obj in page['Contents']:
        extract_logs.append(obj['Key'])


logs_dir = Path.cwd() / 'logs'

date_dir = logs_dir/ str(datetime.date.today())
date_dir.mkdir(exist_ok = True,parents = True)

with open(str(date_dir / 'logs1.json'),"w")  as fp:
    json.dump(extract_logs,fp)


print(datetime.datetime.now())
print(len(extract_logs))

