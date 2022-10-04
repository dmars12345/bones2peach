
import requests as rs
import datetime
from datetime import date
import json
import boto3
def FW_Auth (username,password,filetype):
    import requests as rs
    headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',}
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        }
    response = rs.post('https://api.freewheel.tv/auth/token', headers=headers, data=data).json()
    response['access_token']
    token = 'Bearer ' + response['access_token']
        
    headers = {'accept': 'application/'+str(filetype), 'authorization' : token, 'Content-Type': 'application/'+str(filetype),} 
    return(headers)

auth = {'AWS': {'id': 'id',
  'AWSNONLOGUSER': {'AWSKEY': 'AWSKEY',
   'AWSSKEY': 'AWSSKEY'},
  'AWSLOGUSER': {'AWSLOGUSER': {'AWSKEY': '', 'AWSSKEY': ''}}},
 'FW': {'FWUSER': 'FWUSER',
  'FWPASS': 'FWPASS',
  'MRM': 'MRM'}}

Auth = {"FW" : {} , 'AWS' : {} }

Auth['AWS']['iam'] = {"client": boto3.client('iam',aws_access_key_id =  auth['AWS']['AWSNONLOGUSER']['AWSKEY'], aws_secret_access_key = auth['AWS']['AWSNONLOGUSER']['AWSSKEY']),
               "resource": boto3.resource('iam',aws_access_key_id =  auth['AWS']['AWSNONLOGUSER']['AWSKEY'], aws_secret_access_key = auth['AWS']['AWSNONLOGUSER']['AWSSKEY'])}
Auth['AWS']['s3'] = {"client": boto3.client('s3',aws_access_key_id =  auth['AWS']['AWSNONLOGUSER']['AWSKEY'], aws_secret_access_key = auth['AWS']['AWSNONLOGUSER']['AWSSKEY']),
               "resource": boto3.resource('s3',aws_access_key_id =  auth['AWS']['AWSNONLOGUSER']['AWSKEY'], aws_secret_access_key = auth['AWS']['AWSNONLOGUSER']['AWSSKEY'])}
Auth['AWS']['lambda'] = {"client": boto3.client('lambda',aws_access_key_id =  auth['AWS']['AWSNONLOGUSER']['AWSKEY'], aws_secret_access_key = auth['AWS']['AWSNONLOGUSER']['AWSSKEY'],region_name = 'us-east-1')}

Auth['AWS']['id'] = auth['AWS']['id']

Auth['FW'] = {'xml' : FW_Auth(auth['FW']['FWUSER'],auth['FW']['FWPASS'],'xml'),
              'json' : FW_Auth(auth['FW']['FWUSER'],auth['FW']['FWPASS'],'json'),
              'MRM': auth['FW']['MRM']}


content = 'site_sections'


page = f'https://api.freewheel.tv/services/v4/{content}?per_page=500&page={1}'
#save url
req = rs.get(page,headers=Auth['FW']['json']).json()
name_id_dict = {}
id_name_dict = {}
id_item_dict = {}
#make the list object a variable
total_page = int(req['total_page'])
#save number of iteratins
for x in range(total_page):
    #loop through the number of requests
    it_page =  f'https://api.freewheel.tv/services/v4/{content}?per_page=500&page={x+1}'
    #save the url
    get_page = rs.get(it_page,headers=Auth['FW']['json']).json()['items']
    #make the requests
    for item in get_page:       


        id_name_dict[item['id']] = item['name']

                


IdDump  = json.dumps(id_name_dict)

Nameprefix = f'{content}/' 
Namebucket =  'fw-content-item-ids'

IdFile = f'id_{content}_dict.json'
Auth['AWS']['s3']['resource'].Object(Namebucket,Nameprefix +  IdFile).put(Body = IdDump)
print(datetime.date.today())
