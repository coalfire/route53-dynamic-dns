#!/bin/sh

fifo=/var/run/r53dydns.fifo

# HOSTNAME,1.2.3.4
printf '%s,%s\n' "$common_name" "$ifconfig_pool_remote_ip" >>"$fifo"

# non-zero exit will terminate the connection
exit 0

