#!/bin/bash
cd /root/bones2peaches/user/
aws iam create-policy --policy-name log551-user-access --policy-document file://logaccess.json
aws iam put-user-policy --user-name test43 --policy-name log551-user-access --policy-document file://logaccess.json
aws iam create-policy --policy-name log551-user-ec2-access --policy-document file://ec2_access.json
aws iam put-user-policy --user-name test43 --policy-name log551-user-ec2-access --policy-document file://ec2_access.json
aws iam create-policy --policy-name log551-user-ec2-image-access --policy-document file://ec2_image_access.json
aws iam put-user-policy --user-name test43 --policy-name log551-user-ec2-image-access --policy-document file://ec2_image_access.json
aws iam create-policy --policy-name log551-user-ecr-access --policy-document file://ecr_access.json
aws iam put-user-policy --user-name test43 --policy-name log551-user-ecr-image-access --policy-document file://ecr_access.json
aws iam create-policy --policy-name log551-user-s3-access --policy-document file://s3_access.json
aws iam put-user-policy --user-name test43 --policy-name log551-user-s3-image-access --policy-document file://s3_access.json
cd