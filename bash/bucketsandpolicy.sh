
cd /root/bones2peaches/user/
aws iam create-policy --policy-name log55-user-access --policy-document file://logaccess.json
aws iam put-user-policy --user-name test43 --policy-name log55-user-access --policy-document file://logaccess.json
aws iam create-policy --policy-name log55-user-ec2-access --policy-document file://ec2_access.json
aws iam put-user-policy --user-name test43 --policy-name log55-user-ec2-access --policy-document file://ec2_access.json
aws iam create-policy --policy-name log55-user-ec2-image-access --policy-document file://ec2_image_access.json
aws iam put-user-policy --user-name test43 --policy-name log55-user-ec2-image-access --policy-document file://ec2_image_access.json
aws iam create-policy --policy-name log55-user-ecr-access --policy-document file://ecr_access.json
aws iam put-user-policy --user-name test43 --policy-name log55-user-ecr-image-access --policy-document file://ecr_access.json
aws iam create-policy --policy-name log55-user-s3-access --policy-document file://s3_access.json
aws iam put-user-policy --user-name test43 --policy-name log55-user-s3-image-access --policy-document file://s3_access.json
cd
aws s3 mb s3://freewheel-v4-log-bucket
aws s3api put-public-access-block --bucket freewheel-v4-log-bucket --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
aws s3api put-object --bucket freewheel-v4-log-bucket --key extract/
aws s3api put-object --bucket freewheel-v4-log-bucket --key tansform/
aws s3api put-object --bucket freewheel-v4-log-bucket --key tansform/filteredSlots
aws s3api put-object --bucket freewheel-v4-log-bucket --key tansform/filteredOverlay
aws s3api put-object --bucket freewheel-v4-log-bucket --key tansform/filteredPreroll
aws s3api put-object --bucket freewheel-v4-log-bucket --key tansform/filteredMidroll
aws s3api put-object --bucket freewheel-v4-log-bucket --key load/
aws s3api put-object --bucket freewheel-v4-log-bucket --key load/Midroll
aws s3api put-object --bucket freewheel-v4-log-bucket --key load/Overlay
aws s3api put-object --bucket freewheel-v4-log-bucket --key load/Preroll
aws s3 mb s3://fw-content-item-ids  
aws s3api put-public-access-block --bucket fw-content-item-ids --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
aws s3api put-object --bucket fw-content-item-ids --key series/
aws s3api put-object --bucket fw-content-item-ids --key site_sections/
aws s3api put-object --bucket fw-content-item-ids --key sites/