from pathlib import Path
import json
tf = str(Path.cwd())

with open(tf + '//id.txt','r') as fp:
    id = fp.read()

with open(tf + '//secret.txt','r') as fp:
    secret = fp.read()

aws_id = f"AWSAccessKeyId={id}"
aws_secret = f"AWSSecretKey={secret}"

creds  = ["[test43]", aws_id,aws_secret]
cred_file = open('/root/credentials','w')
for item in creds:
    cred_file.write(item + "\n")

cred_file.close()

config_file = open('/root/config','w')
config = ['[test43]', 'region=us-east-1', 'output=json']
for item in config:
    config_file.write(item + "\n")

config_file.close()


auth_dict = {'UserName': 'test43',
        "AccessKeyId" : id ,
        "SecretAccessKey" : secret}

auth_file = open('/root/loguserkey.json','w')

json.dump(auth_dict,auth_file)
