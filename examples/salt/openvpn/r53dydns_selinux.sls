dynamic-dns-fifo-selinux-context:
  module.run:
    - name: file.set_selinux_context
    - path: /var/run/r53dydns.fifo
    - type: openvpn_var_run_t

selinux_dydns_fifo_type_enforcement:
  file:
    - managed
    - makedirs: True
    - name: /etc/selinux/src/vpnconn_local.te
    - user: root
    - group: root
    - mode: 600
    - source: salt://packages/openvpn/files/selinux_dydns_fifo.te

selinux_dydns_fifo_module:
  cmd.run:
    - cwd: /etc/selinux/src/
    - name: checkmodule -M -m -o vpnconn_local.mod /etc/selinux/src/vpnconn_local.te
    - watch:
      - file: /etc/selinux/src/vpnconn_local.te
    - require:
      - file: /etc/selinux/src/vpnconn_local.te
    - unless: if [ "$(semodule -l | awk '{ print $1 }' | grep vpnconn_local )" == "vpnconn_local" ]; then /bin/true; else /bin/false; fi

selinux_dydns_fifo_package:
  cmd.run:
    - cwd: /etc/selinux/src/
    - name: semodule_package -m vpnconn_local.mod -o vpnconn_local.pp
    - watch:
      - file: /etc/selinux/src/vpnconn_local.te
    - require:
      - file: /etc/selinux/src/vpnconn_local.te
    - unless: if [ "$(semodule -l | awk '{ print $1 }' | grep vpnconn_local )" == "vpnconn_local" ]; then /bin/true; else /bin/false; fi

selinux_dydns_fifo_installed:
  cmd.run:
    - cwd: /etc/selinux/src/
    - name: semodule -i vpnconn_local.pp
    - watch:
      - file: /etc/selinux/src/vpnconn_local.te
    - require:
      - file: /etc/selinux/src/vpnconn_local.te
    - unless: if [ "$(semodule -l | awk '{ print $1 }' | grep vpnconn_local )" == "vpnconn_local" ]; then /bin/true; else /bin/false; fi
