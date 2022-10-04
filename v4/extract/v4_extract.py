import boto3
import gzip
import json
import datetime as datetime
from datetime import date
from pathlib import Path
import sys
from botocore.exceptions import ClientError

auth = str('/root/loguserkey.json')




today = str(datetime.date.today())
with open(auth,'r') as fp:
    creds = json.load(fp)



today = datetime.datetime.today()





root_fw = {'MRM' : 'MRMID'}




sts_client = boto3.client('sts',aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'])


assumed_role_object = sts_client.assume_role(
    RoleArn=f"arn:aws:iam::265086463190:role/{root_fw['MRM']}-V4LogAccess-role",
    RoleSessionName="AssumeRoleSession")

assumed_role_credentials = assumed_role_object['Credentials']

fw_v4_s3_client = boto3.client(
    's3',
    aws_access_key_id=assumed_role_credentials['AccessKeyId'],
    aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
    aws_session_token=assumed_role_credentials['SessionToken'],
)

my_s3_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'])

try:
    response = fw_v4_s3_client.list_objects(
        Bucket='fw-prod-v4logs',
        Prefix=f"{root_fw['MRM']}/v4logs/{str(today.date())}/",
    )


    fwr= boto3.resource('s3',
        aws_access_key_id=assumed_role_credentials['AccessKeyId'],
        aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
        aws_session_token=assumed_role_credentials['SessionToken'],
    )

    s3r = boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],
                aws_secret_access_key=creds['SecretAccessKey'])


    paginator = fw_v4_s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate( Bucket='fw-prod-v4logs',Prefix=f'{root_fw["MRM"]}/v4logs/{str(today.date())}/',)
    logs = []
    for page in pages:
        for obj in page['Contents']:
            logs.append(obj['Key'])
            
except KeyError:
    today = today.replace(day = int(str(today.date()).split(' ')[0].split('-')[-1]) + 1).date()
    print(today)
    response = fw_v4_s3_client.list_objects(
    Bucket='fw-prod-v4logs',
    Prefix=f"{root_fw['MRM']}/v4logs/{str(today.date())}/",)


    fwr= boto3.resource('s3',
        aws_access_key_id=assumed_role_credentials['AccessKeyId'],
        aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
        aws_session_token=assumed_role_credentials['SessionToken'],
    )

    s3r = boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],
                aws_secret_access_key=creds['SecretAccessKey'])


    paginator = fw_v4_s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate( Bucket='fw-prod-v4logs',Prefix=f'{root_fw["MRM"]}/v4logs/{str(today.date())}/',)
    logs = []
    for page in pages:
        for obj in page['Contents']:
            logs.append(obj['Key'])
            


        

my_s3_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
my_paginator = my_s3_client.get_paginator('list_objects_v2')
my_pages = my_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix='extract/'+ str(today.date())+'/',)
my_logs = []
try:
    for page in my_pages:
        for obj in page['Contents']:
            my_logs.append(obj['Key'].split('/')[-1])
    unclaimed = []
    for i in range(len(logs)):
        if logs[i].split('hash')[1].replace('-',"").replace('.gz',"")not in my_logs:
            unclaimed.append(logs[i])
except KeyError:
    unclaimed = logs




        
for x in range(len(unclaimed)):
    item = unclaimed[x]
    log_file = item
    log_extract = log_file.split('hash')[1].replace('-',"").replace('.gz',"")
    log_object = fwr.Object('fw-prod-v4logs', log_file)
    log_stamp = log_file.split('-')[-3]
    try:
        with gzip.GzipFile(fileobj=log_object.get()["Body"]) as gzipfile:
            csv_log = gzipfile.read()       
        resp = s3r.Object('freewheel-v4-log-bucket', 'extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract).put(Body=csv_log)
        print('extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract)
        print(item)
        
    except ClientError:
        try:
            sts_client = boto3.client('sts',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            assumed_role_object = sts_client.assume_role(RoleArn=f"arn:aws:iam::265086463190:role/{root_fw['MRM']}-V4LogAccess-role",RoleSessionName="AssumeRoleSession")
            assumed_role_credentials = assumed_role_object['Credentials']
        
            fw_v4_s3_client = boto3.client( 's3',aws_access_key_id=assumed_role_credentials['AccessKeyId'],aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],aws_session_token=assumed_role_credentials['SessionToken'],)
        
            my_s3_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            response = fw_v4_s3_client.list_objects(Bucket='fw-prod-v4logs',Prefix=f'{root_fw["MRM"]}/v4logs/{str(today.date())}/',)
            fwr= boto3.resource('s3', aws_access_key_id=assumed_role_credentials['AccessKeyId'],aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],aws_session_token=assumed_role_credentials['SessionToken'],)
            s3r = boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            log_object = fwr.Object('fw-prod-v4logs', log_file)
            with gzip.GzipFile(fileobj=log_object.get()["Body"]) as gzipfile:
                csv_log = gzipfile.read()       
            resp = s3r.Object('freewheel-v4-log-bucket', 'extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract).put(Body=csv_log)
            print('extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract)
            print(item)
        
        except ClientError:
            sts_client = boto3.client('sts',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            assumed_role_object = sts_client.assume_role(RoleArn=f"arn:aws:iam::265086463190:role/{root_fw['MRM']}-V4LogAccess-role",RoleSessionName="AssumeRoleSession")
            assumed_role_credentials = assumed_role_object['Credentials']
        
            fw_v4_s3_client = boto3.client( 's3',aws_access_key_id=assumed_role_credentials['AccessKeyId'],aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],aws_session_token=assumed_role_credentials['SessionToken'],)
        
            my_s3_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            response = fw_v4_s3_client.list_objects(Bucket='fw-prod-v4logs',Prefix=f'{root_fw["MRM"]}/v4logs/{str(today.date())}/',)
            fwr= boto3.resource('s3', aws_access_key_id=assumed_role_credentials['AccessKeyId'],aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],aws_session_token=assumed_role_credentials['SessionToken'],)
            s3r = boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
            log_object = fwr.Object('fw-prod-v4logs', log_file)
            with gzip.GzipFile(fileobj=log_object.get()["Body"]) as gzipfile:
                csv_log = gzipfile.read()       
            resp = s3r.Object('freewheel-v4-log-bucket', 'extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract).put(Body=csv_log)
            print('extract' + '/' + str(today.date())  + '/stamp/' + log_stamp +  '/' + log_extract)
            print(item)
            print('TOKEN REFRESH')


