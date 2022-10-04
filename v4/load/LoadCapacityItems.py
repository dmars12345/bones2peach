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


series_content_object = my_s3_resource.Object('fw-content-item-ids','series/id_series_dict.json')
series_file_content = series_content_object.get()['Body'].read().decode('utf-8')
series_dict = json.loads(series_file_content)

sites_content_object = my_s3_resource.Object('fw-content-item-ids','sites/id_sites_dict.json')
sites_file_content = sites_content_object.get()['Body'].read().decode('utf-8')
sites_dict = json.loads(sites_file_content)

site_sections_content_object = my_s3_resource.Object('fw-content-item-ids','site_sections/id_site_sections_dict.json')
site_sections_file_content = site_sections_content_object.get()['Body'].read().decode('utf-8')
site_sections_dict = json.loads(site_sections_file_content)

mapped_overlay_capacity_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
mapped_overlay_capacity_paginator = mapped_overlay_capacity_client.get_paginator('list_objects_v2')
mapped_overlay_capacity_pages = mapped_overlay_capacity_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix=f"transform/filteredOverlay/{today}/mapped/")
item_name = {}
for page in mapped_overlay_capacity_pages:
    for item in page['Contents']:
        if 'Platform' in item['Key']:
            continue
        else:
            json_obj = extract_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket', Key= item['Key'])
            named_dict = json.load(json_obj['Body'] )
            item_name[item['Key'].split('/')[-1]] = named_dict
        

        
new_SiteSection_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
ss_error_counter = 0 
for item in item_name['SiteSection.json']['Impressions']:
    try:
        new_SiteSection_dict['Impressions'][site_sections_dict[item]] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][site_sections_dict[item]] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
    except KeyError:
        ss_error_counter = ss_error_counter + 1
        new_SiteSection_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Overlay/{str(today)}/NamedSiteSections.json").put(Body=json.dumps(new_SiteSection_dict))        

s_error_counter = 0        
new_Site_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['Site.json']['Impressions']:
    try:
        new_Site_dict['Impressions'][sites_dict[item]] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][sites_dict[item]] = item_name['Site.json']['ComericalBreakPatterns'][item]
    except KeyError:
        s_error_counter = s_error_counter + 1
        new_Site_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][f"Error:{s_error_counter}"] = item_name['Site.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Overlay/{str(today)}/NamedSites.json").put(Body=json.dumps(new_Site_dict)) 

se_error_counter = 0        
new_Series_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['series.json']['Impressions']:
    try:
        new_Series_dict['Impressions'][series_dict[item]] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][series_dict[item]] = item_name['series.json']['ComericalBreakPatterns'][item]
    except KeyError:
        se_error_counter = se_error_counter + 1
        new_Series_dict['Impressions'][f"Error:{se_error_counter}"] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][f"Error:{se_error_counter}"] = item_name['series.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Overlay/{str(today)}/NamedSeries.json").put(Body=json.dumps(new_Series_dict)) 


mapped_Midroll_capacity_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
mapped_Midroll_capacity_paginator = mapped_Midroll_capacity_client.get_paginator('list_objects_v2')
mapped_Midroll_capacity_pages = mapped_Midroll_capacity_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix=f"transform/filteredMidroll/{today}/mapped/")
item_name = {}
for page in mapped_Midroll_capacity_pages:
    for item in page['Contents']:
        if 'Platform' in item['Key']:
            continue
        else:
            json_obj = extract_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket', Key= item['Key'])
            named_dict = json.load(json_obj['Body'] )
            item_name[item['Key'].split('/')[-1]] = named_dict
        

        
new_SiteSection_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
ss_error_counter = 0 
for item in item_name['SiteSection.json']['Impressions']:
    try:
        new_SiteSection_dict['Impressions'][site_sections_dict[item]] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][site_sections_dict[item]] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
    except KeyError:
        ss_error_counter = ss_error_counter + 1
        new_SiteSection_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Midroll/{str(today)}/NamedSiteSections.json").put(Body=json.dumps(new_SiteSection_dict))        

s_error_counter = 0        
new_Site_dict  = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['Site.json']['Impressions']:
    try:
        new_Site_dict['Impressions'][sites_dict[item]] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][sites_dict[item]] = item_name['Site.json']['ComericalBreakPatterns'][item]
    except KeyError:
        s_error_counter = s_error_counter + 1
        new_Site_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][f"Error:{s_error_counter}"] = item_name['Site.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Midroll/{str(today)}/NamedSites.json").put(Body=json.dumps(new_Site_dict)) 

se_error_counter = 0        
new_Series_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['series.json']['Impressions']:
    try:
        new_Series_dict['Impressions'][series_dict[item]] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][series_dict[item]] = item_name['series.json']['ComericalBreakPatterns'][item]
    except KeyError:
        se_error_counter = se_error_counter + 1
        new_Series_dict['Impressions'][f"Error:{se_error_counter}"] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][f"Error:{se_error_counter}"] = item_name['series.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Midroll/{str(today)}/NamedSeries.json").put(Body=json.dumps(new_Series_dict)) 

mapped_Preroll_capacity_client = boto3.client('s3',aws_access_key_id=creds['AccessKeyId'],aws_secret_access_key=creds['SecretAccessKey'])
mapped_Preroll_capacity_paginator = mapped_Preroll_capacity_client.get_paginator('list_objects_v2')
mapped_Preroll_capacity_pages = mapped_Preroll_capacity_paginator.paginate( Bucket='freewheel-v4-log-bucket',Prefix=f"transform/filteredPreroll/{today}/mapped/")
item_name = {}
for page in mapped_Preroll_capacity_pages:
    for item in page['Contents']:
        if 'Platform' in item['Key']:
            continue
        else:
            json_obj = extract_s3_client.get_object(Bucket= 'freewheel-v4-log-bucket', Key= item['Key'])
            named_dict = json.load(json_obj['Body'] )
            item_name[item['Key'].split('/')[-1]] = named_dict
        

        
new_SiteSection_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
ss_error_counter = 0 
for item in item_name['SiteSection.json']['Impressions']:
    try:
        new_SiteSection_dict['Impressions'][site_sections_dict[item]] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][site_sections_dict[item]] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
    except KeyError:
        ss_error_counter = ss_error_counter + 1
        new_SiteSection_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['Impressions'][item]
        new_SiteSection_dict['ComericalBreakPatterns'][f"Error:{ss_error_counter}"] = item_name['SiteSection.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Preroll/{str(today)}/NamedSiteSections.json").put(Body=json.dumps(new_SiteSection_dict))        

s_error_counter = 0        
ew_Site_dict  = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['Site.json']['Impressions']:
    try:
        new_Site_dict['Impressions'][sites_dict[item]] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][sites_dict[item]] = item_name['Site.json']['ComericalBreakPatterns'][item]
    except KeyError:
        s_error_counter = s_error_counter + 1
        new_Site_dict['Impressions'][f"Error:{ss_error_counter}"] = item_name['Site.json']['Impressions'][item]
        new_Site_dict['ComericalBreakPatterns'][f"Error:{s_error_counter}"] = item_name['Site.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Preroll/{str(today)}/NamedSites.json").put(Body=json.dumps(new_Site_dict)) 

se_error_counter = 0        
new_Series_dict = {'Impressions': {}, 'ComericalBreakPatterns': {}}
for item in item_name['series.json']['Impressions']:
    try:
        new_Series_dict['Impressions'][series_dict[item]] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][series_dict[item]] = item_name['series.json']['ComericalBreakPatterns'][item]
    except KeyError:
        se_error_counter = se_error_counter + 1
        new_Series_dict['Impressions'][f"Error:{se_error_counter}"] = item_name['series.json']['Impressions'][item]
        new_Series_dict['ComericalBreakPatterns'][f"Error:{se_error_counter}"] = item_name['series.json']['ComericalBreakPatterns'][item]
my_s3_resource.Object('freewheel-v4-log-bucket', f"load/Preroll/{str(today)}/NamedSeries.json").put(Body=json.dumps(new_Series_dict))