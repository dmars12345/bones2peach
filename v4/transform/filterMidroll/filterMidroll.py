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
auth = str('/root/loguserkey.json')

today = str(datetime.date.today())
with open(auth,'r') as fp:
    creds = json.load(fp)

transform_logs_dir = Path.cwd()  / 'logs'
transform_date_dir = transform_logs_dir/ today
transform_date_dir.mkdir(exist_ok = True,parents = True)

with open(str(transform_date_dir / 'logs1.json'),'r') as fp:
    logs= json.load(fp)


my_s3_resource =boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'])

my_s3_client =boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'])


parsed_slot_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
parsed_slot_paginator = parsed_slot_client.get_paginator('list_objects_v2')
parsed_slot_pages = parsed_slot_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix=f"transform/filteredSlots/{str(today)}/csv/")


for log in logs:
    log = log.split('/')[-1]
    extracted_overlay_file  = my_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket',
                                        Key= f"transform/filteredSlots/{today}/csv/{log}")
    slot_impressions_log = pd.read_csv(extracted_overlay_file['Body'],low_memory=False)
    Midroll_slots = slot_impressions_log[slot_impressions_log['TimePositionClass'].str.contains('midroll',na=False)].reset_index()

    Midroll_dict = {}
    for d in range(len(Midroll_slots)):
        MaxAds = int(str(Midroll_slots['MaxAds'][d]).split('.')[0])
        MaxDuration = int(str(Midroll_slots['MaxDuration'][d]).split('.')[0])
        TimeUnfilled = int(str(Midroll_slots['TimeUnfilled'][d]).split('.')[0])
        AdsSelected =int(str( Midroll_slots['AdsSelected'][d]).split('.')[0])
        AdDuration = int(str(Midroll_slots['AdDuration'][d]).split('.')[0])
        SiteId = str(Midroll_slots['SiteId'][d]).split('.')[0]
        SiteSectionId = str(Midroll_slots['SiteSectionId'][d]).split('.')[0]
        SeriesId = str(Midroll_slots['SeriesId'][d]).split('.')[0]
        VideoAssetId =str(Midroll_slots['VideoAssetId'][d]).split('.')[0]
        PlatformDeviceId = str(Midroll_slots['PlatformDeviceId'][d]).split('.')[0]
        temp_dict = {'MaxAds':  MaxAds,
              'MaxDuration' : MaxDuration,
              'TimeUnfilled' :TimeUnfilled,
              'AdsSelected ': AdsSelected ,
              'AdDuration': AdDuration,
                'SiteId': SiteId,
                'SiteSectionId':SiteSectionId,
                'SeriesId':SeriesId,
                'VideoAssetsId': VideoAssetId,
                'PlatformDeviceId': PlatformDeviceId}
        Midroll_dict[Midroll_slots['TransactionId'][d]] = temp_dict 

    output ={'capacity' : {'AdOpportunities': int(Midroll_slots['MaxDuration'].sum()),'MissedOpportunities': int(Midroll_slots['TimeUnfilled'].sum())}}
    print(datetime.datetime.now())
    print(output['capacity'])

    for item in  Midroll_dict.keys():

        output['capacity']['MonetizedInventory'] = output['capacity']['AdOpportunities']
        output['capacity']['UnsoldInventory'] =output['capacity']['MissedOpportunities']
        output['capacity']['SellThru'] = 1 - (output['capacity']['MissedOpportunities']
                                                             / output['capacity']['AdOpportunities'])
    output_dict = {'perItem': Midroll_dict, 'summary': output}
    my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredMidroll/{str(today)}/json/{log.replace('.csv','.json')}").put(Body=json.dumps(output_dict))