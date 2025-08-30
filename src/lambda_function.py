import boto3
import datetime
import os

ec2 = boto3.client('ec2')

# Get SG ID from environment variable
QUARANTINE_SG_ID = os.environ.get("QUARANTINE_SG_ID")

def lambda_handler(event, context):
    try:
        # Getting instance ID from GuardDuty event
        instance_id = event['detail']['resource']['instanceDetails']['instanceId']
        print(f"Quarantining instance: {instance_id}")

        # Initial quarantine tag
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[{"Key": "status", "Value": "quarantined"}]
        )

        # Additional compromised tags
        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {'Key': 'Compromised', 'Value': 'True'},
                {'Key': 'DetectedAt', 'Value': datetime.datetime.utcnow().isoformat() + "Z"}
            ]
        )
        print(f"Tagged instance {instance_id} as Compromised")
        
        # Applying quarantine SG
        if not QUARANTINE_SG_ID:
            raise Exception("QUARANTINE_SG_ID environment variable not set")

        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[QUARANTINE_SG_ID]
        )
        print(f"Instance {instance_id} isolated with SG {QUARANTINE_SG_ID}")
        
        return {
            "statusCode": 200,
            "body": f"Instance {instance_id} quarantined and tagged"
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": str(e)
        }
