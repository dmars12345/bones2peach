import sys
import os
import json
from pathlib import Path
import boto3
import datetime as datetime
from datetime import date
import io
from io import StringIO
from collections import ChainMap


today = str(datetime.date.today())
auth = str('/root/loguserkey.json')

with open(auth,'r') as fp:
    creds = json.load(fp)

    
extract_s3_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'] 
        )
my_s3_resource =boto3.resource('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])

unmapped_overlay_cappacity_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
unmapped_overlay_cappacity_paginator = unmapped_overlay_cappacity_client.get_paginator('list_objects_v2')
unmapped_overlay_cappacity_pages = unmapped_overlay_cappacity_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix=f"transform/filteredOverlay/{today}/json/")
per = []
agg = []
for page in unmapped_overlay_cappacity_pages:
    counter = 0 
    for item in page['Contents']:
        json_obj_log = extract_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket', Key= item['Key'])
        json_log = json.load(json_obj_log['Body'] )
        per.append(json_log['perItem'])
        counter = counter + 1
        agg.append({counter: json_log['summary']})
        

total_summary = dict(ChainMap(*agg))
total_per_item = dict(ChainMap(*per))


video_series = []
for key in total_per_item:
    video_series.append(total_per_item[key]['SeriesId'])
series = list(set(video_series))

series_dict = {}

for item in series:
    series_dict[item] = {'MaxAds': 0 ,'AdsSelected':0,'TimeUnfilled': 0,'AdDuration':0,'MaxDuration':0,'CBP' : 0}
    
total_duration = 0
total_selected = 0
for item in total_per_item:
    series_dict[total_per_item[item]['SeriesId']]['MaxAds']= series_dict[total_per_item[item]['SeriesId']]['MaxAds'] + total_per_item[item]['MaxAds']
    series_dict[total_per_item[item]['SeriesId']]['AdsSelected'] = series_dict[total_per_item[item]['SeriesId']]['AdsSelected'] + total_per_item[item]['AdsSelected ']
    series_dict[total_per_item[item]['SeriesId']]['TimeUnfilled'] = series_dict[total_per_item[item]['SeriesId']]['TimeUnfilled']+ total_per_item[item]['TimeUnfilled'] 
    series_dict[total_per_item[item]['SeriesId']]['AdDuration'] =     series_dict[total_per_item[item]['SeriesId']]['AdDuration']  + total_per_item[item] ['AdDuration']
    series_dict[total_per_item[item]['SeriesId']]['MaxDuration'] = series_dict[total_per_item[item]['SeriesId']]['MaxDuration'] +     total_per_item[item] ['MaxDuration']
    series_dict[total_per_item[item]['SeriesId']]['CBP'] = series_dict[total_per_item[item]['SeriesId']]['CBP']  + (len(total_per_item[item])/ len(total_per_item[item]))
    total_duration = total_duration + total_per_item[item]['AdDuration']
    total_selected = total_selected + total_per_item[item]['AdsSelected ']
 
average_creative_duration = total_duration / total_selected
series_impression_dict = {}
for x in range(len(list(series_dict.keys()))):
    CapacityInImp = series_dict[list(series_dict.keys())[x]]['MaxDuration'] / average_creative_duration 
    UnfilledInImp = series_dict[list(series_dict.keys())[x]]['TimeUnfilled'] / average_creative_duration 
    SoldInImp =  CapacityInImp - UnfilledInImp
    series_impression_dict[list(series_dict.keys())[x]] = {'Capacity' : CapacityInImp, 'Unsold' : UnfilledInImp ,'Sold': SoldInImp}
    
series_output = {'Impressions' : series_impression_dict,
                'ComericalBreakPatterns' : series_dict}


my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredOverlay/{str(today)}/mapped/series.json").put(Body=json.dumps(series_output))


video_Site = []
for key in total_per_item:
    video_Site.append(total_per_item[key]['SiteId'])
Site = list(set(video_Site))

Site_dict = {}

for item in Site:
    Site_dict[item] = {'MaxAds': 0 ,'AdsSelected':0,'TimeUnfilled': 0,'AdDuration':0,'MaxDuration':0,'CBP' : 0}
    
total_duration = 0
total_selected = 0
for item in total_per_item:
    Site_dict[total_per_item[item]['SiteId']]['MaxAds']= Site_dict[total_per_item[item]['SiteId']]['MaxAds'] + total_per_item[item]['MaxAds']
    Site_dict[total_per_item[item]['SiteId']]['AdsSelected'] = Site_dict[total_per_item[item]['SiteId']]['AdsSelected'] + total_per_item[item]['AdsSelected ']
    Site_dict[total_per_item[item]['SiteId']]['TimeUnfilled'] = Site_dict[total_per_item[item]['SiteId']]['TimeUnfilled']+ total_per_item[item]['TimeUnfilled'] 
    Site_dict[total_per_item[item]['SiteId']]['AdDuration'] =     Site_dict[total_per_item[item]['SiteId']]['AdDuration']  + total_per_item[item] ['AdDuration']
    Site_dict[total_per_item[item]['SiteId']]['MaxDuration'] = Site_dict[total_per_item[item]['SiteId']]['MaxDuration'] +     total_per_item[item] ['MaxDuration']
    Site_dict[total_per_item[item]['SiteId']]['CBP'] = Site_dict[total_per_item[item]['SiteId']]['CBP']  + (len(total_per_item[item])/ len(total_per_item[item]))
    total_duration = total_duration + total_per_item[item]['AdDuration']
    total_selected = total_selected + total_per_item[item]['AdsSelected ']
 
average_creative_duration = total_duration / total_selected
Site_impression_dict = {}
for x in range(len(list(Site_dict.keys()))):
    CapacityInImp = Site_dict[list(Site_dict.keys())[x]]['MaxDuration'] / average_creative_duration 
    UnfilledInImp = Site_dict[list(Site_dict.keys())[x]]['TimeUnfilled'] / average_creative_duration 
    SoldInImp =  CapacityInImp - UnfilledInImp
    Site_impression_dict[list(Site_dict.keys())[x]] = {'Capacity' : CapacityInImp, 'Unsold' : UnfilledInImp ,'Sold': SoldInImp}
    
Site_output = {'Impressions' : Site_impression_dict,
                'ComericalBreakPatterns' : Site_dict}


my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredOverlay/{str(today)}/mapped/Site.json").put(Body=json.dumps(Site_output))

video_SiteSection = []
for key in total_per_item:
    video_SiteSection.append(total_per_item[key]['SiteSectionId'])
SiteSection = list(set(video_SiteSection))

SiteSection_dict = {}

for item in SiteSection:
    SiteSection_dict[item] = {'MaxAds': 0 ,'AdsSelected':0,'TimeUnfilled': 0,'AdDuration':0,'MaxDuration':0,'CBP' : 0}
    
total_duration = 0
total_selected = 0
for item in total_per_item:
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['MaxAds']= SiteSection_dict[total_per_item[item]['SiteSectionId']]['MaxAds'] + total_per_item[item]['MaxAds']
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['AdsSelected'] = SiteSection_dict[total_per_item[item]['SiteSectionId']]['AdsSelected'] + total_per_item[item]['AdsSelected ']
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['TimeUnfilled'] = SiteSection_dict[total_per_item[item]['SiteSectionId']]['TimeUnfilled']+ total_per_item[item]['TimeUnfilled'] 
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['AdDuration'] =     SiteSection_dict[total_per_item[item]['SiteSectionId']]['AdDuration']  + total_per_item[item] ['AdDuration']
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['MaxDuration'] = SiteSection_dict[total_per_item[item]['SiteSectionId']]['MaxDuration'] +     total_per_item[item] ['MaxDuration']
    SiteSection_dict[total_per_item[item]['SiteSectionId']]['CBP'] = SiteSection_dict[total_per_item[item]['SiteSectionId']]['CBP']  + (len(total_per_item[item])/ len(total_per_item[item]))
    total_duration = total_duration + total_per_item[item]['AdDuration']
    total_selected = total_selected + total_per_item[item]['AdsSelected ']
 
average_creative_duration = total_duration / total_selected
SiteSection_impression_dict = {}
for x in range(len(list(SiteSection_dict.keys()))):
    CapacityInImp = SiteSection_dict[list(SiteSection_dict.keys())[x]]['MaxDuration'] / average_creative_duration 
    UnfilledInImp = SiteSection_dict[list(SiteSection_dict.keys())[x]]['TimeUnfilled'] / average_creative_duration 
    SoldInImp =  CapacityInImp - UnfilledInImp
    SiteSection_impression_dict[list(SiteSection_dict.keys())[x]] = {'Capacity' : CapacityInImp, 'Unsold' : UnfilledInImp ,'Sold': SoldInImp}
    
SiteSection_output = {'Impressions' : SiteSection_impression_dict,
                'ComericalBreakPatterns' : SiteSection_dict}


my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredOverlay/{str(today)}/mapped/SiteSection.json").put(Body=json.dumps(SiteSection_output))

video_PlatformDevice = []
for key in total_per_item:
    video_PlatformDevice.append(total_per_item[key]['PlatformDeviceId'])
PlatformDevice = list(set(video_PlatformDevice))

PlatformDevice_dict = {}

for item in PlatformDevice:
    PlatformDevice_dict[item] = {'MaxAds': 0 ,'AdsSelected':0,'TimeUnfilled': 0,'AdDuration':0,'MaxDuration':0,'CBP' : 0}
    
total_duration = 0
total_selected = 0
for item in total_per_item:
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['MaxAds']= PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['MaxAds'] + total_per_item[item]['MaxAds']
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['AdsSelected'] = PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['AdsSelected'] + total_per_item[item]['AdsSelected ']
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['TimeUnfilled'] = PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['TimeUnfilled']+ total_per_item[item]['TimeUnfilled'] 
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['AdDuration'] =     PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['AdDuration']  + total_per_item[item] ['AdDuration']
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['MaxDuration'] = PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['MaxDuration'] +     total_per_item[item] ['MaxDuration']
    PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['CBP'] = PlatformDevice_dict[total_per_item[item]['PlatformDeviceId']]['CBP']  + (len(total_per_item[item])/ len(total_per_item[item]))
    total_duration = total_duration + total_per_item[item]['AdDuration']
    total_selected = total_selected + total_per_item[item]['AdsSelected ']
 
average_creative_duration = total_duration / total_selected
PlatformDevice_impression_dict = {}
for x in range(len(list(PlatformDevice_dict.keys()))):
    CapacityInImp = PlatformDevice_dict[list(PlatformDevice_dict.keys())[x]]['MaxDuration'] / average_creative_duration 
    UnfilledInImp = PlatformDevice_dict[list(PlatformDevice_dict.keys())[x]]['TimeUnfilled'] / average_creative_duration 
    SoldInImp =  CapacityInImp - UnfilledInImp
    PlatformDevice_impression_dict[list(PlatformDevice_dict.keys())[x]] = {'Capacity' : CapacityInImp, 'Unsold' : UnfilledInImp ,'Sold': SoldInImp}
    
PlatformDevice_output = {'Impressions' : PlatformDevice_impression_dict,
                'ComericalBreakPatterns' : PlatformDevice_dict}


my_s3_resource.Object('freewheel-v4-log-bucket', f"transform/filteredOverlay/{str(today)}/mapped/PlatformDevice.json").put(Body=json.dumps(PlatformDevice_output))