import boto3
import logging

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
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch=batch
            )
        logging.info(response)
        return response
    except Exception as e:
        logging.warn(e)


def set_up_log(filename='/var/log/route53_dydns.log', level=logging.DEBUG):
    logging.basicConfig(filename=filename,level=level)


def main():        
    set_up_log()
    pass



if __name__ == '__main__':
    main()
