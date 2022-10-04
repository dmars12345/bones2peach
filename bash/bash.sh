sudo apt install needrestart
sudo needrestart -u NeedRestart::UI::stdio -r a
git clone "CLONEURL"
mv /root/bones2peaches/bash/terraform.sh /root/terraform.sh
sudo chmod +x terraform.sh
/.terraform.sh
mv /root/bones2peaches/bash/aws.sh /root/aws.sh
sudo chmod +x aws.sh
mv /root/bones2peaches/bash/roles.sh /root/roles.sh
sudo chmod +x roles.sh
/.roles.sh
mv /root/bones2peaches/bash/buckets.sh /root/buckets.sh
sudo chmod +x buckets.sh
/.buckets.sh
mv /root/bones2peaches/bash/roles.sh /root/roles.sh
sudo chmod +x roles.sh
/.roles.sh
mv /root/bones2peaches/bash/docker.sh /root/docker.sh
sudo chmod +x docker.sh
/.docker.sh
mv /root/bones2peaches/bash/cron.sh /root/cron.sh
sudo chmod +x cron.sh
./cron.sh
cd /root/bones2peaches/tf
python3 aws.py
cd /root/bones2peaches/v4/extract







