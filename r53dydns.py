#!/usr/bin/env python3

import datetime
import logging
import os
import yaml

import boto3
import configargparse

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
    logging.info(zone + str(batch))
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch=batch
            )
        logging.info(response)
        return response
    except Exception as e:
        logging.error(e)

def set_up_log(filename='/var/log/route53_dydns.log', level='WARN'):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level)

    logging.basicConfig(
        filename=filename,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=numeric_level,
        datefmt='%Y%m%dT%H:%M:%S'
    )


def read_fifo_and_request(fifo, zone, domain, wait_time):
    changes = []
    begin_time = datetime.datetime.now()
    with open(fifo) as pipeline:
        while True:
            data = pipeline.readline()
            if len(data) == 0:
                break

            try:
                data = data.rstrip()
                hostname, ip = data.split(',')
                fqdn = hostname + domain
                record_change = change(fqdn, ip)
                changes.append(record_change)

            except Exception as e:
                logging.error(e)

    delta =  datetime.datetime.now() - begin_time 
    if delta.seconds > wait_time:
        batch = change_batch(changes)
        request_change_resource_record_set(zone, batch)
        return

def main():        
    parser = configargparse.ArgumentParser(
        default_config_files=['/etc/r53dydns.conf']
        )
    parser.add_argument(
        '-c',
        '--config',
        help='Use config file CONFIG',
        is_config_file=True,
        default='/etc/r53dydns.conf',
        action='store',
        dest='config',
        )
    parser.add_argument(
        '-L',
        '--log-file',
        help='Use log-file LOG_FILE',
        default='/var/log/route53_dydns.log',
        action='store',
        dest='log_file',
        )
    parser.add_argument(
        '-l',
        '--log-level',
        help='Log at level LOG_LEVEL, one of NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL',
        default='INFO',
        action='store',
        dest='log_level',
        )
    parser.add_argument(
        '-f',
        '--file',
        help='read from file FILE (most likely a fifo)',
        default='/var/run/vpn-dydns.fifo',
        action='store',
        dest='fifo',
        )
    parser.add_argument(
        '-d',
        '--domain',
        help='append domain DOMAIN to incoming hostnames, eg: example.com',
        default='',
        action='store',
        dest='domain',
        )
    parser.add_argument(
        '-z',
        '--zone',
        help='upsert record sets to Hosted Zone Id ZONE',
        default='',
        action='store',
        dest='zone',
        )
    parser.add_argument(
        '-w',
        '--wait-time',
        help='wait TIME seconds between posting records to route53',
        type=int,
        default=1,
        action='store',
        dest='wait_time',
        )

    args = parser.parse_args()
    set_up_log(filename=args.log_file, level=args.log_level)

    while True:
        read_fifo_and_request(args.fifo, args.zone, args.domain, args.wait_time)

if __name__ == '__main__':
    main()
