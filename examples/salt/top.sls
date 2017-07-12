# Master file_roots configuration:

base:
  'openvpn-*':
    - openvpn.server
    - r53dydns.sls
    - r53dydns_dependencies.sls
    - r53dydns_selinux.sls
