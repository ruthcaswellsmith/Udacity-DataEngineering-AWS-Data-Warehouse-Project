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

redshift.delete_cluster(ClusterIdentifier=config.CLUSTER, SkipFinalClusterSnapshot=True)
