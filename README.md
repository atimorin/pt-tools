# pt-tools

vpuser@vp:/tmp/pt-tools$ python nmap-parser.py -h
Usage: nmap-parser.py [options]

Options:
  -h, --help            show this help message and exit
  -p PORTS, --ports=PORTS
                        interesting ports, comma separated. both tcp and udp
  --exportports         export hosts to files by inetersting ports
  -w WORKDIR, --workdir=WORKDIR
                        working directory. default is 'input'
  -o OUTPUTDIR, --outputdir=OUTPUTDIR
                        output directory. default is 'output'
vpuser@vp:/tmp/pt-tools$ python nmap-parser.py -w ~/bb/yandex/ --exportports -p 80,443,21,22,10000,8080,81,8081,8000
'workdir: /home/vpuser/bb/yandex'
'process file: /home/vpuser/bb/yandex/tcp.80.443.hosts.gnmap'
'process file: /home/vpuser/bb/yandex/some.hosts.gnmap'
'process file: /home/vpuser/bb/yandex/87.250.224-255.0-255.gnmap'
'process file: /home/vpuser/bb/yandex/jdwp.gnmap'
'process file: /home/vpuser/bb/yandex/213.180.192-223.0-255.gnmap'
'process file: /home/vpuser/bb/yandex/yandex.nets.ipv4.jdwp.gnmap'
vpuser@vp:/tmp/pt-tools$ ls -la output/
total 56
drwxr-xr-x 2 vpuser vpuser  4096 Jun 29 13:40 .
drwxr-xr-x 4 vpuser vpuser  4096 Jun 29 13:39 ..
-rw-r--r-- 1 vpuser vpuser  2804 Jun 29 13:40 hosts.tcp.443
-rw-r--r-- 1 vpuser vpuser  2538 Jun 29 13:40 hosts.tcp.80
-rw-r--r-- 1 vpuser vpuser    43 Jun 29 13:40 hosts.tcp.8000
-rw-r--r-- 1 vpuser vpuser    58 Jun 29 13:40 hosts.tcp.8080
-rw-r--r-- 1 vpuser vpuser  6576 Jun 29 13:40 list_hosts.csv
-rw-r--r-- 1 vpuser vpuser 14702 Jun 29 13:40 open_by_hosts.csv
-rw-r--r-- 1 vpuser vpuser  8107 Jun 29 13:40 open_by_ports.csv
