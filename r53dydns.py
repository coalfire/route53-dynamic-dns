import boto3

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

def record_set(changes, comment='created by route53-dydns'):
    return {
        "Comment": comment,
        "Changes": changes
    }


