include:
  - .

openvpn-server-config:
  file.managed:
    - source: 
      - salt://openvpn/files/server.conf
    - name: /etc/openvpn/server.conf
    - user: nobody
    - group: nobody
    - mode: 755
    - template: jinja

openvpn-service:
  service.running:
    - name: openvpn@server
    - enable: True
    - require:
      - pkg: openvpn-package
      - file: custom-openvpn-service-file

custom-openvpn-service-file:
  file.managed:
    - source:
      - salt://packages/openvpn/files/openvpn.service
    - name: /etc/systemd/system/openvpn@.service
    - user: root
    - group: root
    - mode: 640

ip-forwarding:
  sysctl.present:
    - name: net.ipv4.ip_forward
    - value: 1
    - config: /etc/sysctl.d/50-ip_forward.conf

