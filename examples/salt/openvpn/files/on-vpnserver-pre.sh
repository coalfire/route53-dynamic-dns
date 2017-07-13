#!/bin/sh

fifo=/var/run/r53dydns.fifo
context='unconfined_u:object_r:openvpn_var_run_t:s0'
mode=664

mkfifo --context="$context" --mode="$mode" "$fifo"
chown nobody:nobody "$fifo"

# openvpn server will not start if an ExecStartPre script fails
exit 0
