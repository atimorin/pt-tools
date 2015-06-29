import os,sys,re
from os.path import join as jpath, abspath
from pprint import pprint
import optparse

__author__        = "atimorin"
__version__        = "1.3"

csv_export = True
list_export = True # export to list host;tcp:port1,port2,...;udp:port1,port2,..
csv_line_separate = True
csv_delimiter = '\t'
#csv_delimiter = ';'

open_tcp_ports = {}
open_udp_ports = {}
all_hosts = {}

class Host(object):

    def __init__(self, host):
        self.host = host
        self.tcp_ports = {}
        self.udp_ports = {}

    def add_tcp_port(self, port, service_banner):
        if not self.tcp_ports.has_key(port):
            self.tcp_ports[port] = service_banner
    
    def add_udp_port(self, port, service_banner):
        if not self.udp_ports.has_key(port):
            self.udp_ports[port] = service_banner


class OpenPort(object):

    def __init__(self, port_number, proto):
        self.port_number = int(port_number)
        self.proto = proto
        self.hosts = {}

    def add_host(self, host, service_banner=''):
        if host and not self.hosts.has_key(host):
            self.hosts[host] = service_banner
        elif host and self.hosts.has_key(host) and service_banner and not self.hosts[host]:
            self.hosts[host] = service_banner

    def get_hosts(self):
        hosts = set(self.hosts.keys())
        return hosts

    def get_banner_by_host(self, host):
        return self.hosts[host]


def add_host(host):
    if not all_hosts.has_key(host):
        h = Host(host)
        all_hosts[host] = h


def parse_open_ports_string(data):
    open_ports = []
    d = re.findall(r'Ports: (.*)', data)
    if d:
        d = d[0]
        d2 = re.findall(r'[0-9]{1,5}/open/(?:tc|ud)p//(?:.*)//', d)
        if d2:
            d2 = d2[0]
            t = d2.split(',')
            for el in t:
                el = el.strip()
                port,status,proto,ignore,service_banner,ignore2 = el.split('/', 5)
                #if port and status=='open' and proto and service_banner:
                if status == 'open':
                    if ignore2 != '//' or len(ignore2)>=4:
                        ignore2 = ignore2.replace('/', '')
                        service_banner = '%s , %s' % (service_banner, ignore2)
                    open_ports.append((int(port), proto, service_banner))
    return open_ports

def process_file(filename):

    for l in open(filename, 'r'):
        l = l.strip()
        host = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', l)
        host = host and host[0] or None
        if host:
            #open_ports = re.findall(r'([0-9]{1,5}\/open\/)(tcp|udp)', l)
            open_ports = parse_open_ports_string(l)
            if open_ports:
                for (port, proto, service_banner) in open_ports:
                    #port = int(port.split('/')[0])
                    if proto == 'tcp':
                        if not open_tcp_ports.has_key(port):
                            op = OpenPort(port, 'tcp')
                            op.add_host(host, service_banner)
                            open_tcp_ports[port] = op
                        else:
                            open_tcp_ports[port].add_host(host, service_banner)
                    else:
                        if not open_udp_ports.has_key(port):
                            op = OpenPort(port, 'udp')
                            op.add_host(host, service_banner)
                            open_udp_ports[port] = op
                        else:
                            open_udp_ports[port].add_host(host, service_banner)




if __name__ == '__main__':

    parser = optparse.OptionParser()
    parser.add_option('-p', '--ports', dest="ports", help="interesting ports, comma separated. both tcp and udp")
    parser.add_option('--exportports', dest="exportports", action="store_true", default=False, help="export hosts to files by inetersting ports")
    parser.add_option('-w', '--workdir', dest="workdir", default="input", help="working directory. default is 'input' ")
    parser.add_option('-o', '--outputdir', dest="outputdir", default="output", help="output directory. default is 'output' ")

    options, args = parser.parse_args()

    workdir = abspath(options.workdir)
    outputdir = abspath(options.outputdir)
    #if not outputdir:
    #    outputdir = abspath(os.curdir)
    interesting_ports = options.ports
    exportports = options.exportports
    
    if interesting_ports:
        interesting_ports = [ int(p) for p in interesting_ports.split(',') ]
    
    pprint('workdir: %s' % workdir)
    for root, dirs, files in os.walk(workdir):
        for filename in files:
            if filename.endswith('.gnmap'):
                filename = abspath(jpath(workdir, filename))
                pprint('process file: %s' % filename)
                process_file(filename)
    
    tcp_ports = open_tcp_ports.keys()
    tcp_ports.sort()

    udp_ports = open_udp_ports.keys()
    udp_ports.sort()

    if csv_export:
        out_fh = open(abspath(jpath(outputdir, 'open_by_ports.csv')), 'w')
        out_fh.write('TCP{0}\n'.format(csv_delimiter))
        for port in tcp_ports:
            if interesting_ports and port not in interesting_ports:
                continue
            op = open_tcp_ports[port]
            hosts = op.get_hosts()
            out_fh.write('{0}{1}\n'.format(port, csv_delimiter))
            for host in hosts:
                add_host(host)
                service_banner = op.get_banner_by_host(host)
                out_fh.write('{0}{1}{2}{3}\n'.format(csv_delimiter,host,csv_delimiter, service_banner) )
                all_hosts[host].add_tcp_port(port, service_banner)
                if exportports:
                    fn = abspath(jpath(outputdir, 'hosts.tcp.{0}'.format(port)))
                    open(fn, 'w').write('\n'.join(hosts))
            if csv_line_separate:
                out_fh.write('*****{0}*****{1}*****{2}\n'.format(csv_delimiter,csv_delimiter,csv_delimiter))
        out_fh.write('\n')

        out_fh.write('UDP{0}\n'.format(csv_delimiter))
        for port in udp_ports:
            if interesting_ports and port not in interesting_ports:
                continue
            op = open_udp_ports[port]
            hosts = op.get_hosts()
            out_fh.write('{0}{1}\n'.format(port, csv_delimiter))
            for host in hosts:
                add_host(host)
                service_banner = op.get_banner_by_host(host)
                out_fh.write('{0}{1}{2}{3}\n'.format(csv_delimiter,host,csv_delimiter, service_banner) )
                all_hosts[host].add_udp_port(port, service_banner)
                if exportports:
                    fn = abspath(jpath(outputdir, 'hosts.udp.{0}'.format(port)))
                    open(fn, 'w').write('\n'.join(hosts))
            if csv_line_separate:
                out_fh.write('*****{0}*****{1}*****{2}\n'.format(csv_delimiter,csv_delimiter,csv_delimiter))
        out_fh.write('\n')

        out_fh = open(abspath(jpath(outputdir, 'open_by_hosts.csv')), 'w')
        list_fh = open(abspath(jpath(outputdir, 'list_hosts.csv')), 'w')
        for (host_str, host) in all_hosts.items():
            out_fh.write('{0}{1}{2}\n\n'.format(host_str,csv_delimiter, csv_delimiter))
            
            out_fh.write('TCP{0}{1}\n'.format(csv_delimiter, csv_delimiter))
            tcp_ports = host.tcp_ports.keys()
            tcp_ports.sort()
            for port in tcp_ports:
                service_banner = host.tcp_ports[port]
                out_fh.write('{0}{1}{2}{3}\n'.format(csv_delimiter, port, csv_delimiter, service_banner) )
            #if csv_line_separate:
            #    out_fh.write('*****{0}*****{1}*****{2}\n'.format(csv_delimiter,csv_delimiter,csv_delimiter))
            #out_fh.write('\n')

            out_fh.write('UDP{0}{1}\n'.format(csv_delimiter, csv_delimiter))
            udp_ports = host.udp_ports.keys()
            udp_ports.sort()
            for port in udp_ports:
                service_banner = host.udp_ports[port]
                out_fh.write('{0}{1}{2}{3}\n'.format(csv_delimiter, port, csv_delimiter, service_banner) )
            if csv_line_separate:
                out_fh.write('*****{0}*****{1}*****{2}\n'.format(csv_delimiter,csv_delimiter,csv_delimiter))
            #out_fh.write('\n')

            list_hosts = '{0};tcp:{1};udp:{2}\n'.format(host_str, ','.join(map(lambda x: str(x), tcp_ports)), ','.join(map(lambda x: str(x), udp_ports)))
            list_fh.write(list_hosts)





