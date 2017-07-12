openvpn-server-client-connect-script:
  file.managed:
    - source: 
      - salt://packages/openvpn/files/on-vpnclient-connect.sh
    - name: /usr/local/bin/on-vpnclient-connect
    - makedirs: True
    - user: nobody
    - group: nobody
    - mode: 755

dynamic-dns-fifo:
  file.mknod:
    - name: /var/run/r53dydns.fifo
    - ntype: p
    - user: nobody
    - group: nobody
    - mode: 664
