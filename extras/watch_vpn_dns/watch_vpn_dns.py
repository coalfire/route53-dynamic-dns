#!/usr/bin/env python3

import logging
from time import sleep
from collections import namedtuple

from dns.resolver import query
import dns
import configargparse

Status = namedtuple('Status', ['name', 'ip'])

def set_up_log(filename='/var/log/watch_vpn_dns.log', level='WARN'):
    """
    Accept optional filename, level.
    Create a logger.
    """
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % level)

    logging.basicConfig(
        filename=filename,
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=numeric_level,
        datefmt='%Y%m%dT%H:%M:%S',
    )


def _get_status_lines(status_files):
    """
    Accept status files (list of file-like objects),
    Return generator of lines startign with "CLIENT_LIST,"
    """
    for status_file in status_files:
        with open(status_file) as fileh:
            for line in fileh:
                if line.startswith("CLIENT_LIST,"):
                    yield line.strip()


def _parse_status(status_line):
    """
    Accept status line (str).
    Return namedtuple Status of name and ip.
    """
    name_field = 1
    ip_field = 3
    fields = status_line.split(",")
    return Status(name=fields[name_field], ip=fields[ip_field])


def ips_from_vpn(status_files):
    """
    Accept status_files (list of file-like objects).
    Return dict of name: ip
    """
    status_lines = _get_status_lines(status_files)
    statuses = [_parse_status(line) for line in status_lines]
    return {
        status.name: status.ip
        for status in statuses
        if status.name != "UNDEF" and status.ip != ""
    }


def dig_record(name, domain):
    """
    Accept name (str),
    domain (str).
    Return ip of name's A record in domain,
    or None if there is none.
    """
    record = name + domain
    try:
        answer = query(record, "A")[0].to_text()
    except dns.resolver.NXDOMAIN:
        answer = None
    logging.debug(f"{name}{domain} returned {answer}")
    return answer


def ips_from_dns(names, domain):
    """
    Accept names (list of common_names),
    domain (str).
    Return dict of common_name: ip.
    """
    return {
        name: dig_record(name, domain)
        for name in names
    }


def diff(what_should_be, what_is):
    """
    Accept what_should_be (dict of name: ip)
    and what_is (dict of name: ip)
    Return dict of name: ip with ip from 'what_should_be' where 'what_is' does
    not match 'what_should_be'.
    """
    return {
        name: ip
        for name, ip in what_should_be.items()
        if what_should_be[name] != what_is.get(name, None)
    }


def send_to_pipe(fifo, to_update):
    """
    Accept fifo (file-like object) and to_update (dict of common_name, ip).
    Send to_update as key:value pair to fifo.
    Return True on success,
    otherwise raise Exception.
    """
    logging.info('Updating: ' + str(to_update))
    with open(fifo, "w") as pipe:
        for name, ip in to_update.items():
            pipe.write(name + "," + ip + "\n")


def reconcile_dns(status_files, fifo, domain):
    """
    Accept status files (list of file-like objects),
    fifo (a file, presumable a pipe, to write to),
    domain (str).
    Send DNS records for update to pipe based  n VPN status.
    """
    from_vpn = ips_from_vpn(status_files)
    logging.debug(f"IPs should be: {from_vpn}")
    from_dns = ips_from_dns(from_vpn.keys(), domain)
    logging.debug(f"IPs from dns: {from_dns}")
    to_update = diff(from_vpn, from_dns)
    logging.debug(f"To update: {to_update}")
    if to_update:
        send_to_pipe(fifo, to_update)


def main():
    """
    Parse arguments, initialize logging, and enter main loop.
    """
    parser = configargparse.ArgumentParser(
        default_config_files=["/etc/watch-vpn-dns.conf"]
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Use config file CONFIG",
        is_config_file=True,
        default="/etc/watch-vpn-dns.conf",
        action="store",
        dest="config",
    )
    parser.add_argument(
        "-L",
        "--log-file",
        help="Use log-file LOG_FILE",
        default="/var/log/watch_vpn_dns.log",
        action="store",
        dest="log_file",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        help="Log at level LOG_LEVEL, one of NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL",
        default="INFO",
        action="store",
        dest="log_level",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="write to FILE (most likely a fifo)",
        default="/var/run/vpn-dydns.fifo",
        action="store",
        dest="fifo",
    )
    parser.add_argument(
        "-s",
        "--status_file",
        help="read from status file(s) STATUS",
        action="append",
        dest="status",
    )
    parser.add_argument(
        "-d",
        "--domain",
        help="append domain DOMAIN to incoming hostnames, eg: example.com",
        default="",
        action="store",
        dest="domain",
    )
    parser.add_argument(
        "-w",
        "--wait-time",
        help="wait TIME seconds between posting records to route53",
        type=int,
        default=60,
        action="store",
        dest="wait_time",
    )

    args = parser.parse_args()
    set_up_log(filename=args.log_file, level=args.log_level)

    logging.info(args)
    while True:
        reconcile_dns(args.status, args.fifo, args.domain)
        sleep(args.wait_time)


if __name__ == "__main__":
    main()
