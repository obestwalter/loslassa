apt-packages:
  pkg.installed:
    - names:
      #- python2.7-dev
      - python-pip
      #- build-essential
    - refresh: False

pip-requirements:
  pip.installed:
    - requirements: /vagrant/requirements.txt
    - require:
      - pkg: apt-packages
