"""This script requires the following env vars to be set
- AWS_REGION
- AWS_KEY_ID
- AWS_SECRET_KEY
- DB_PORT
"""

import boto3

from settings import config

ec2 = boto3.resource('ec2',
                     region_name=config.AWS_REGION,
                     aws_access_key_id=config.AWS_KEY_ID,
                     aws_secret_access_key=config.AWS_SECRET_KEY
                     )

try:
    vpc = ec2.Vpc(id='vpc-06c34ea036874e6bc')
    defaultSg = list(vpc.security_groups.all())[0]
    print(defaultSg)

    defaultSg.authorize_ingress(
        GroupName=defaultSg.group_name,
        CidrIp='0.0.0.0/0',
        IpProtocol='TCP',
        FromPort=int(config.DB_PORT),
        ToPort=int(config.DB_PORT)
    )
except Exception as e:
    print(e)
