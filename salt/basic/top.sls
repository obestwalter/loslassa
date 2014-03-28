basic-packages:
  pkg.installed:
    - names:
      - python2.7-dev
      - python-pip
      - acpid
      #- libssl-dev  # todo still needed ... by who?
      - build-essential
    - refresh: False
