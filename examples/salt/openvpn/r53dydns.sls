openvpn-server-client-connect-script:
  file.managed:
    - source: 
      - salt://packages/openvpn/files/on-vpnclient-connect.sh
    - name: /usr/local/bin/on-vpnclient-connect
    - makedirs: True
    - user: nobody
    - group: nobody
    - mode: 755

dynamic-dns-service:
  service.running:
    - name: r53dydns
    - enable: True
    - require:
      - file: dynamic-dns-config
      - file: dynamic-dns-service-file

dynamic-dns-service-file:
  file.managed:
    - source:
      - salt://packages/openvpn/files/r53dydns.service
    - name: /etc/systemd/system/r53dydns.service
    - user: root
    - group: root
    - mode: 640

dynamic-dns-config:
  file.managed:
    - source: 
      - salt://packages/openvpn/files/r53dydns.conf
    - name: /etc/r53dydns.conf
    - user: root
    - group: nobody
    - mode: 640

dynamic-dns-fifo:
  file.mknod:
    - name: /var/run/r53dydns.fifo
    - ntype: p
    - user: nobody
    - group: nobody
    - mode: 664
