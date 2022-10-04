#!/bin/bash
$nrconf{restart} = 'l'
sudo apt-get install pip -y
sudo apt-get install python-pip -y
sudo apt-get -y install python3-boto3 
sudo apt-get -y install python3-pandas 
sudo apt-get update -y
sudo apt-get install cron -y
(crontab -l ; echo "0 * * * * python3 /root/v4/extract/PumpLogsStart/PumpLogsStart.py >> /root/v4/extract/PumpLogsStart/cronlogs/PumpLogsStart.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 */2 * * * python3 /root/v4/extract/PumpSlotStartLogs/PumpSlotStartLogs.py >> /root/v4/extract/PumpSlotStartLogs/cronlogs/PumpSlotStartLogs.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 19 * * * python3 /root/v4/tansform/filterMidroll/filterMidroll.py >> /root/v4/tansform/filterMidroll/cronlogs/filterMidroll.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 19 * * * python3 /root/v4/tansform/filterOverlay/filterOverlay.py >> /root/v4/tansform/filterOverlay/cronlogs/filterOverlay.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 19 * * * python3 /root/v4/tansform/filterPreroll/filterPreroll.py >> /root/v4/tansform/filterPreroll/cronlogs/filterPreroll.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 21 * * * python3 /root/v4/tansform/MidrollByItem/MidrollByItem.py >> /root/v4/tansform/MidrollByItem/cronlogs/filterMidrollByItem.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 21 * * * python3 /root/v4/tansform/OverlayByItem/OverlayByItem.py >> /root/v4/tansform/OverlayByItem/cronlogs/filterOverlayByItem.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "0 21 * * * python3 /root/v4/tansform/PrerollByItem/PrerollByItem.py >> /root/v4/tansform/PrerollByItem/cronlogs/filterPrerollByItem.log 2>&1") | sort - | uniq - | crontab -
(crontab -l ; echo "30 22 * * * python3 /root/v4/extract/LoadCapacityItems.py >> /root/v4/extract/cronlogs/LoadCapacityItems.py.log 2>&1") | sort - | uniq - | crontab -