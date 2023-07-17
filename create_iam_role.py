"""This script requires the following env vars to be set
- AWS_REGION
- AWS_KEY_ID
- AWS_SECRET_KEY
"""

import boto3
import json
from settings import config

IAM_ROLE_NAME = 'dwhrole'

# Create client for IAM
iam = boto3.client('iam',
                   region_name=config.AWS_REGION,
                   aws_access_key_id=config.AWS_KEY_ID,
                   aws_secret_access_key=config.AWS_SECRET_KEY
                   )

# STEP 1: IAM ROLE so Redshift can access S#
try:
    print('1.1 Creating a new IAM Role')
    role = iam.create_role(
        Path='/',
        RoleName=IAM_ROLE_NAME,
        Description='Allows Redshift clusters to call AWS services.',
        AssumeRolePolicyDocument=json.dumps(
            {'Statement': [{'Action': 'sts:AssumeRole',
                            'Effect': 'Allow',
                            'Principal': {'Service': 'redshift.amazonaws.com'}}
                           ],
             'Version': '2012-10-17'}
        )
    )
    print(role)

except Exception as e:
    print(e)

# Attach Policy
print('1.2 Attaching Policy')
response = iam.attach_role_policy(
    RoleName=IAM_ROLE_NAME,
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")

print(response['ResponseMetadata']['HTTPStatusCode'])
