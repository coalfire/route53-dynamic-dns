import boto3

client = boto3.client('route53')

def change(fqdn, ip):
    return {
        "Action": "UPSERT",
        "ResourceRecordSet": {
            "Name": fqdn,
            "Type": "A",
            "TTL": 180,
            "ResourceRecords": [
                {
                    "Value": ip
                },
            ],
        }
    }

def change_batch(changes, comment='created by route53-dydns'):
    return {
        "Comment": comment,
        "Changes": changes
    }

def request_change_resource_record_set(zone, batch):
    response = client.change_resource_record_sets(
        HostedZoneId=zone,
        ChangeBatch=batch
        )
    return response
