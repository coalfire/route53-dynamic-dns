python34_pip_package:
  pkg:
    - installed
    - name: python34-pip

python34_package:
  pkg:
    - installed
    - name: python34

boto3_package:
  pip.installed:
    - require:
      - pkg: python34_pip_package
    - bin_env: '/bin/pip3'
    - name: boto3 == 1.4.4

ConfigArgParse_package:
  pip.installed:
    - require:
      - pkg: python34_pip_package
    - bin_env: '/bin/pip3'
    - name: ConfigArgParse == 0.12.0

PyYAML_package:
  pip.installed:
    - require:
      - pkg: python34_pip_package
    - bin_env: '/bin/pip3'
    - name: PyYAML == 3.12

