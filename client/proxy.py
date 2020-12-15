from scapy.all import *
from threading import *
import socket

statuses = {
    0:"need to accept",
    1:"connect accepted",
    2:"1+server conn",
    3:"only server conn"
}
server_conn = ("127.0.0.1",10000)

my_vir_ip = "127.0.0.1"
ips = ["127.0.0.1", "168.192.1.1", "168.192.1.5", "80.75.12.212"]

class Proxy():
    def __init__(self, data):
        self.cln_dt = data
        self.thrd_conn = []
        print("start:")
        sniff(lfilter=self.out_routing, prn=self.prnt)
        print("end!")

    def out_routing(self, p):
        global my_vir_ip
        global ips
        if IP in p and TCP in p:
            return p[TCP].flags=='S' and p[IP].dst in ips 
        else:
            return False

    def in_routing(self, p):
        global my_vir_ip
        global ips
        if IP in p:
            p[IP].dst == my_vir_ip

    def port_taken(self, port):
        for c in self.thrd_conn:
            if port == c.my_addr[1]:
                return True
        return False

    def prnt(self, p):
        print(p.show())
        print("send to => " + p[IP].dst)
        if not self.port_taken(p[TCP].dport):
            pkt = Ether(dst=p[Ether].src, src=p[Ether].dst)/IP(src=p[IP].dst ,dst=p[IP].src)/TCP(flags="SA", dport=p[TCP].sport, sport=p[TCP].dport)
            pkt[TCP].seq=50
            pkt[TCP].ack = p[TCP].seq+1
            print(pkt.show())
            sr(pkt)
            self.thrd_conn.append(ThirdPartyConnection(('', p[TCP].dport), (p[IP].src, p[TCP].sport)))
            self.thrd_conn[-1].setName("ip="+p[IP].dst+"|port="+str(p[TCP].dport))
            self.thrd_conn[-1].start()




class ThirdPartyConnection(Thread):
    """
    new socket with the server
    and one with the third party applicatin
    make communication between them
    """
    def __init__(self, to_conn, from_conn):
        super(ThirdPartyConnection, self).__init__()
        self.app_sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_addr = to_conn
        self.app_addr = from_conn
        self.app_sock_s.bind(to_conn)
        self.app_sock_s.listen(2)
        self.status = statuses[0]

    def accespt_app(self):
        try:
            #self.app_sock_c, self.app_addr = self.app_sock_s.accept()
            pkt = Ether()/IP(src=self.my_addr[0] ,dst=self.app_addr[0])/TCP(flags="SA")
            print("connect to app")
            self.status = statuses[1]
            self.connect_to_server()
            self.status = statuses[2]
        except Exception as e:
            print(str(e))
            print("can't make a fully connection")


    def connect_to_server(self):
        self.serv_sock.connect(server_conn)

    def run(self):
        self.accespt_app()
        print("my new sock with app-> " + self.app_sock_c)

if __name__ == '__main__':
    prx = Proxy(" ")