import ipaddress
import re
import platform
import subprocess
import socket
from tabulate import tabulate


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0


def get_host_info(host):
    name = ''
    ip = ''
    match = re.search(r'([0-9]{1,3}[\.]){3}[0-9]{1,3}', host)
    if match:  # передали IP
        ip = host
        try:
            host_name = socket.gethostbyaddr(ip)
            if hostName:
                name = host_name[0]
        except Exception:
            name = ''
    else:  # передали имя
        name = host
        ip = socket.gethostbyname(name)
    return ip, name


def host_ping(address_list):
    for host in address_list:
        ip_str, name = get_host_info(host)
        address = ipaddress.ip_address(ip_str)
        print(f'ip {address}, name "{name}", {"Узел доступен" if ping(host) else "Узел не доступен"}')


def host_range_ping(segment1, segment2, segment3, segment4_start, segment4_end):
    host_list = []
    for segment4 in range(segment4_start, segment4_end + 1):
        ip4_segments = [str(segment1), str(segment2), str(segment3), str(segment4)]
        ip4 = ipaddress.ip_address('.'.join(ip4_segments))
        host_list.append(str(ip4))
    if host_list:
        host_ping(host_list)


def host_range_ping_tab(segment1, segment2, segment3, segment4_start, segment4_end):
    reachable_host_list = []
    unreachable_host_list = []
    for segment4 in range(segment4_start, segment4_end + 1):
        ip4_segments = [str(segment1), str(segment2), str(segment3), str(segment4)]
        ip_str = '.'.join(ip4_segments)
        ip4 = ipaddress.ip_address(ip_str)
        if ping(ip_str):
            reachable_host_list.append(ip_str)
        else:
            unreachable_host_list.append(ip_str)
    if reachable_host_list or unreachable_host_list:
        maxlen = max(len(reachable_host_list), len(unreachable_host_list))
        host_list = []
        reachable_host_list.reverse()
        unreachable_host_list.reverse()
        for i in range(maxlen):
            try:
                r_elem = reachable_host_list.pop()
            except Exception:
                r_elem = ''
            try:
                u_elem = unreachable_host_list.pop()
            except Exception:
                u_elem = ''
            host_list.append({'Reachable': r_elem, 'Unreachable': u_elem})

        print(tabulate(host_list, headers='keys'))


print('=' * 50)
host_ping(['ya.ru', '192.168.0.1', 'localhost'])

print('=' * 50)
host_range_ping(192, 168, 1, 0, 2)

print('=' * 50)
host_range_ping_tab(10, 1, 0, 0, 2)
