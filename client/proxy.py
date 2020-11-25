from scapy.all import *

def routing(p, my_vir_ip, ips : list):
    return p[IP].dst in ips or p[IP].dst == my_vir_ip