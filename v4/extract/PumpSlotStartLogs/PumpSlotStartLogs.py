import sys
import os
import json
from pathlib import Path
import boto3
import datetime as datetime
from datetime import date
import io
from io import StringIO
import pandas as pd
today = str(datetime.date.today())
auth = str('/root/loguserkey.json')

with open(auth,'r') as fp:
    creds = json.load(fp)
extract_logs_dir = Path.cwd() / 'v4' / 'extract' / 'logs'
extract_date_dir = extract_logs_dir/ str(datetime.date.today())
my_s3_resource =boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
my_s3_client =boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
with open(str(extract_date_dir / 'logs1.json'),'r') as fp:
     que_logs = json.load(fp)
for remaining_log in que_logs:
    print(remaining_log)
    extracted_log = my_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket', Key= remaining_log)
    log_df = pd.read_csv(extracted_log['Body'],low_memory = False)
    slot_impressions_log = log_df[log_df['EventName'].str.contains('slotImpression',na=False)]
    slot_impressions_df = pd.DataFrame()
    slot_impressions_df['TransactionId'] = slot_impressions_log['TransactionId']
    slot_impressions_df['TimePositionClass'] = slot_impressions_log['TimePositionClass']
    slot_impressions_df['MaxAds'] = slot_impressions_log['MaxAds'].astype(int)
    slot_impressions_df['MaxDuration'] = slot_impressions_log['MaxDuration'].astype(int)
    slot_impressions_df['TimeUnfilled'] = slot_impressions_log['TimeUnfilled'].astype(int)
    slot_impressions_df['AdsSelected'] = slot_impressions_log['AdsSelected'].astype(int)
    slot_impressions_df['AdDuration'] = slot_impressions_log['AdDuration'].astype(int)
    slot_impressions_df['SiteId'] = slot_impressions_log['SiteId'].astype(str)
    slot_impressions_df['SiteSectionId'] = slot_impressions_log['SiteSectionId'].astype(str)
    slot_impressions_df['SeriesId'] = slot_impressions_log['SeriesId'].astype(str)
    slot_impressions_df['VideoAssetId'] = slot_impressions_log['VideoAssetId'].astype(str)
    slot_impressions_df['PlatformDeviceId'] = slot_impressions_log['PlatformDeviceId'].astype(str)
    csv_buffer = io.StringIO()
    slot_impressions_df.to_csv(csv_buffer)
    slot_response = my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredSlots/{str(today)}/csv/{remaining_log.split('/')[-1]}").put(Body=csv_buffer.getvalue())
    print(slot_response)
    print({f"transform/filteredSlots/{str(today)}/csv/{remaining_log.split('/')[-1]}" : datetime.datetime.now()})
    print(datetime.datetime.now())