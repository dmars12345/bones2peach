# bones2peaches

problem --------------------------------------------------------------------------------------------------------------------------------------------------

The freewheel v4 log files is a digital media publishers rawest form of data. This data is used by many departments in an online publisher's organization.
Being able to implement a datapipeline that is reliable and captures all key points of the raw data is pivotal for any data driven media sales strategy.
 
solution -------------------------------------------------------------------------------------------------------------------------------------------------
 
The bones2peaches framework requires root user credentials of an AWS account authorized by freewheel to have access to the log file data and
a freewheel user name and password which has been authenticated for api access. With these basic requirements , the bones2peaches framework is able to 
set up and automated the ETL datapipeline. a security group and ssh_key is also needed.
 
bones2peaches file tree -----------------------------------------------------------------------------------------------------------------------------------
|init.py
| ---> bash\ ---> aws.sh
| ---> bash\ ---> docker.sh
| ---> bash\ ---> cron.sh
| ---> bash\ ---> buckets.sh
| ---> bash\ ---> terraform.sh
| ---> bash\ ---> roles.sh
| ---> resources\ ---> ecr.json
| ---> resources\ ---> ecrrole.json
| ---> tf\ ---> aws.py
| ---> tf\ ---> creds
| ---> tf\ ---> output.tf
| ---> tf\ ---> providers.tf
| ---> tf\ ---> user.tf
| ---> user\ ---> anayltics_ec2_image_access.json
| ---> user\ ---> ec2_access.json
| ---> user\ ---> ec2_image_access.json
| ---> user\ ---> ecr_access.json
| ---> user\ ---> ecs_access.json
| ---> user\ ---> logaccess.json
| ---> user\ ---> roledoc.json
| ---> user\ ---> route_53_access.json
| ---> user\ ---> s3_access.json
| ---> v4\ ---> extract\ ---> v4_extract.py
| ---> v4\ ---> extract\ ---> PumpSlotStartLogs.py
| ---> v4\ ---> extract\ ---> PumpSlotStartLogs.cron
| ---> v4\ ---> extract\ ---> PumpSlotStartLogs ---> cronlogs\
| ---> v4\ ---> extract\ ---> PumpLogsStart.py
| ---> v4\ ---> extract\ ---> PumpLogsStart.cron
| ---> v4\ ---> extract\ ---> PumpLogsStart ---> cronlogs\
| ---> v4\ ---> transform\ ---> filteredMidroll ---> filteredMidroll.py
| ---> v4\ ---> transform\ ---> filteredMidroll ---> filteredMidroll.cron
| ---> v4\ ---> transform\ ---> filteredMidroll ---> cronlogs\
| ---> v4\ ---> transform\ ---> filteredPreroll ---> filteredPreroll.py
| ---> v4\ ---> transform\ ---> filteredPreroll ---> filteredPreroll.cron
| ---> v4\ ---> transform\ ---> filteredPreroll ---> cronlogs\
| ---> v4\ ---> transform\ ---> filteredOverlay ---> filteredOverlay.py
| ---> v4\ ---> transform\ ---> filteredOverlay ---> filteredOverlay.cron
| ---> v4\ ---> transform\ ---> filteredOverlay ---> cronlogs\
| ---> v4\ ---> transform\ ---> MidrollByItem ---> MidrollByItem.py
| ---> v4\ ---> transform\ ---> MidrollByItem ---> MidrollByItem.cron
| ---> v4\ ---> transform\ ---> MidrollByItem ---> cronlogs\
| ---> v4\ ---> transform\ ---> PrerollByItem ---> PrerollByItem.py
| ---> v4\ ---> transform\ ---> PrerollByItem ---> PrerollByItem.cron
| ---> v4\ ---> transform\ ---> PrerollByItem ---> cronlogs\
| ---> v4\ ---> transform\ ---> OverlayByItem ---> OverlayByItem.py
| ---> v4\ ---> transform\ ---> OverlayByItem ---> OverlayByItem.cron
| ---> v4\ ---> transform\ ---> OverlayByItem ---> cronlogs\
| ---> v4\ ---> load\ ---> ids\ ---> series\ ---> crontab
| ---> v4\ ---> load\ ---> ids\ ---> series\ ---> Dockerfile
| ---> v4\ ---> load\ ---> ids\ ---> series\ ---> series.py
| ---> v4\ ---> load\ ---> ids\ ---> site_sections\ ---> site_sections.py
| ---> v4\ ---> load\ ---> ids\ ---> sites\ ---> sites.py
| ---> v4\ ---> load\ ---> LoadByCapacity.py
| ---> v4\ ---> load\ ---> LoadByCapacity.cron
| ---> v4\ ---> load\ ---> cronlogs


Code High Level Overview -----------------------------------------------------------------------------------------------------------------------------------------------
 
Git clone the bones2peaches repo on your computer and pass in the security group id into the __init__.py file.
 
When you run this file a new ec2 instance is started with a user data script. The user datascript will used python/awscli to set up cloud infrastructue.
_________________________________________________________________________________________________________________________________________________________________________
terraform.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
uses downloads terraforms command line tool on to the instance, creates a new Iam user and generates security credentials and saves them in the
instances root directory in a json file which all of the etl scripts use to authenticate from.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
role.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
the script locates the json files in the  bones2peaches/user/ directioary and uses awscli to attach and create roles that get assigned the user
created in the terraform.sh script
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
buckets.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
uses awscli to create the neccessary s3 buckets used to store the data from the pipeline and also makes the buckets not publically accessable.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
cron.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
installs crontab, pip, boto3 and pandas onto the ec2 instance. The script also sets all up neccessary cron schedules used to automate the pipeline.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
docker.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
creates an ecr for the images used within the pipeline. alo builds and pushes the containers used within the pipeline to ecr.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
aws.sh
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
installs awscli and authenticates as the root user.



Data Pipeline Overview ---------------------------------------------------------------------------------------------------------------------------------------------------

Extract ------------------------------------------------------------------------------------------------------------------------------------------------------------------

as soon as the cloud infrascturture has been initalized the v4_extract.py file starts running. The reason why there is no cron schedule for this file
is because the code will run perpetually. All this code does is move the convert the gzip csv log file into a csv and moves the file from freewheel's bucket
into our s3 bucket.

next the PumpLogsStart.py python file ques up logs file for the PumpSlotStartLogs.py file.

The PumpSlotStartLogs.py gets rid of the fluff in the raw log files and breaks down the core data points needed for meaningful insights.

see below for the change in data types:
np.int64 ---> int
np.int64 ---> str


Transform ------------------------------------------------------------------------------------------------------------------------------------------------------------------

once the log files fluff has been filtered out, the data is then broken down into three categories, overlay, midroll and preroll and is then converted tojson.

for the filter python files, this takes the csv file from the PumpSlotStartLogs.py and filters the dataframe for overlay, midroll and preroll. 

after the dataframe has been filtered, the file is converted into a json file and converts advertising seconds into capacity,

monetized inventory and unsold inventory in aggregate.

after the category has been filtered in aggregate next comes the CapacityByItem.

This takes the data from the filtered python file and then breaks the same metrics out by sites, site_sections and series.

Load ------------------------------------------------------------------------------------------------------------------------------------------------------------------

after each category has been broken out by item, the last thing to do is to convert the item id  into a name.

The code queries the dictionary from the respective s3 bucket and converts the id into a name so the user can see capacity by series_names,
site_name or site_section_name.


