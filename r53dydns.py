import boto3
import logging
from logging.handlers import SysLogHandler
import time

from service import find_syslog, Service

class DNSUpdateService(Service):
    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)

    def run(self):
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(1)

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
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = DNSUpdateService('DNS_update_service', pid_dir='/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print "DNSUpdateService is running."
        else:
            print "DNSUpdateService is not running."
    else:
        sys.exit('Unknown command "%s".' % cmd)
