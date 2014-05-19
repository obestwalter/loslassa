include:
  - basic

/usr/bin/loslassa:
  file.managed:
    - source: salt://loslassa/loslassa
    - user: vagrant
    - group: vagrant
    - mode: 0777
    - requires:
      - sls: basic

loslassa:
  cmd.run:
    - name: loslassa
    - requires:
      - file: /usr/bin/loslassa
