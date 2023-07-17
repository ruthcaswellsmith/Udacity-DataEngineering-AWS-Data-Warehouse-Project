"""This script requires the following env vars to be set
- AWS_REGION
- AWS_KEY_ID
- AWS_SECRET_KEY
- CLUSTER
"""

import boto3
from settings import config

redshift = boto3.client('redshift',
                        region_name=config.AWS_REGION,
                        aws_access_key_id=config.AWS_KEY_ID,
                        aws_secret_access_key=config.AWS_SECRET_KEY
                        )


myClusterProps = redshift.describe_clusters(ClusterIdentifier=config.CLUSTER)['Clusters'][0]

cluster_status = myClusterProps['ClusterStatus']
print(f"Cluster is {cluster_status}")

if cluster_status == 'available':
    print(f"Host is {myClusterProps['Endpoint']['Address']}")
    print(f"Role ARN is {myClusterProps['IamRoles'][0]['IamRoleArn']}")
    print(f"VpcID is {myClusterProps['VpcId']}")