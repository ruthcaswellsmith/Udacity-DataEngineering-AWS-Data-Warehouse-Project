"""This script requires the following env vars to be set
- AWS_REGION
- AWS_KEY_ID
- AWS_SECRET_KEY
- DB_NAME
- DB_USER
- DB_PASSWORD
- CLUSTER
- SECURITY_GROUP_ID
- IAM_ROLE_ARN
"""

import boto3
from settings import config

DWH_CLUSTER_TYPE = 'multi-node'
DWH_NUM_NODES = '4'
DWH_NODE_TYPE = 'dc2.large'

redshift = boto3.client('redshift',
                        region_name=config.AWS_REGION,
                        aws_access_key_id=config.AWS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_KEY,
                        )

try:
    response = redshift.create_cluster(
        # HW
        ClusterType=DWH_CLUSTER_TYPE,
        NodeType=DWH_NODE_TYPE,
        NumberOfNodes=int(DWH_NUM_NODES),

        # Identifiers and Credentials
        DBName=config.DB_NAME,
        ClusterIdentifier=config.CLUSTER,
        MasterUsername=config.DB_USER,
        MasterUserPassword=config.DB_PASSWORD,

        # Roles
        IamRoles=[config.IAM_ROLE_ARN],

        # Security Groups
        VpcSecurityGroupIds=[config.SECURITY_GROUP_ID]
    )

except Exception as e:
    print(e)
