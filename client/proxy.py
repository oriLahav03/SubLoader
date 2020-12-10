from scapy.all import *

my_vir_ip = "127.0.0.1"
ips = ["127.0.0.1", "168.192.1.1", "168.192.1.5", "25.200.2.86"]
def routing(p):
    global my_vir_ip
    global ips
    if IP in p:
        return p[IP].dst in ips or p[IP].dst == my_vir_ip
    else:
        return False

def prnt(p):
    print(p.summary())
    print("send to => " + p[IP].dst)

print("start:")
sniff(lfilter=routing, prn=prnt)
print("end")