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

  file.managed:
    - name: /home/vagrant/.bashrc
    - text: export PYTHONPATH=/vagrant/loslassa


/home/vagrant/.bashrc:
  file.managed:
    - source: salt://basic/.bashrc
    - user: vagrant
    - group: vagrant
    - mode: 644

source-bashrc:
  cmd.run:
    - name: source /home/vagrant/.bashrc
    - requires:
      - file: /home/vagrant/.bashrc
