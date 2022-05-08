import re
import sys
import traceback
from dns.resolver import resolve
import xml.etree.ElementTree as ET
import CommandHandler
from Store import ConfigStore


def resolve_dns(domain, record='A'):
    ips = []
    try:
        for ip in resolve(domain, record):
            ips.append(str(ip))
        return ips
    except Exception as e:
        print(e, file=sys.stderr)
        return ips

class ExtFunctions:

    @staticmethod
    def commandHandler():
        return CommandHandler.CommandHandler()

    @staticmethod
    def output(io, *args):
        if isinstance(io, str):
            ConfigStore.updateConfig(io, *args)
        else:
            print(*args, file=io)

    @staticmethod
    def resolve_dns_for_domains(stdout, stderr, inFile, out_format='{domain},{ips}', delimiter='\n'):
        try:
            resolved = {}
            
            # with open(file_name, 'r') as file:
            for line in inFile.read().split(delimiter):
                resolved[line] = resolve_dns(line)
            for domain in resolved.keys():
                ips = resolved[domain]
                out = out_format.format(domain=domain, ips=",".join(ips))
                ExtFunctions.output(stdout, out)
        except Exception:
            ExtFunctions.output(stderr, traceback.format_exc())

    @staticmethod
    def getPortsFromNmapScan(stdout, stderr, inFile, domain_ip_map_file_name=None, out_format= '{ip},{ports}'):
        try:
            tree = ET.parse(inFile)
            root = tree.getroot()

            hosts = {}
            for host in root.iter('host'):
                for ports in host.iter('ports'):
                    for port in ports.iter('port'):
                        ip = host.find('address').attrib['addr']
                        status = port.find('state').attrib['state']
                        portId = port.attrib['portid']
                        if status == "open":
                            current = hosts.get(ip, [])
                            current.append(portId)
                            hosts[ip] = current
            domain_ip_map = {}
            if domain_ip_map_file_name:
                with open(domain_ip_map_file_name, 'r') as file:
                    for line in file.readlines():
                        line = line.strip()
                        domain, *ips = line.split(',')
                        domain_ip_map[domain] = ips
                        
            for ip in hosts.keys():
                content = out_format.format(ip=ip, ports=','.join(hosts.get(ip)))
                ExtFunctions.output(stdout, content)

                for domain in domain_ip_map.keys():
                    if ip in domain_ip_map[domain]:
                        content = out_format.format(ip=domain, ports=','.join(hosts.get(ip)))
                        ExtFunctions.output(stdout, content)


        except Exception:
            ExtFunctions.output(stderr, traceback.format_exc())

    @staticmethod
    def foreach_exec(command, out, err, command_stdin, loop_input, extractVariables=None, delimiter='\n',):
        with open(loop_input, 'r') as file:
            for line in file.read().split(delimiter):
                if not len(line):
                    continue
                for key in extractVariables.keys():
                    ConfigStore.updateConfig(key, re.search(extractVariables[key], line).group(1))

                cmd = list(map(lambda x:x.format_map(ConfigStore.config.get('variables')), command))
                ExtFunctions.commandHandler().exec_command(cmd, out, err, command_stdin)