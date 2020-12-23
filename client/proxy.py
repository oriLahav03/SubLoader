from scapy.all import *
from threading import Thread
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
        sniff(lfilter=self.out_routing, prn=self.new_con_o)
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
            return p[IP].dst == my_vir_ip or p[TCP].sport == 10000

    def port_taken(self, port):
        for c in self.thrd_conn:
            if port == c.srv_addr[1]:
                return True
        return False

    def new_con_o(self, p):
        print(p.show())
        print("send to => " + p[IP].dst)
        if not self.port_taken(p[TCP].dport):
            pkt = Ether(dst=p[Ether].src, src=p[Ether].dst)/IP(src=p[IP].dst ,dst=p[IP].src)/TCP(flags="SA", dport=p[TCP].sport, sport=p[TCP].dport)
            pkt[TCP].seq=50
            pkt[TCP].ack = p[TCP].seq+1
            print(pkt.show())
            sr(pkt)
            new_app = ThirdPartyConnection(('', p[TCP].dport), (p[IP].src, p[TCP].sport))
            new_app.setName("ip="+p[IP].dst+"|port="+str(p[TCP].dport))
            new_app.accespt_app()
            new_app.start()
            self.thrd_conn.append(new_app)

    def new_con_i(self, p):
        """
        docstring
        """
        raw = p[Raw].load.decode()
        if raw[:2]=='60':
            key = raw[2:]
            new_app = ThirdPartyConnection((p[IP].dst, p[TCP].dport), (p[IP].src, p[TCP].sport))
            new_app.connect_app()
            new_app.start()
            self.thrd_conn.append(new_app)



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
        self.srv_addr = to_conn
        self.app_addr = from_conn
        self.app_sock_s.bind(to_conn)
        self.app_sock_s.listen(1)
        self.status = statuses[0]

    def accespt_app(self):
        try:
            #self.app_sock_c, self.app_addr = self.app_sock_s.accept()
            pkt = Ether()/IP(src=self.srv_addr[0] ,dst=self.app_addr[0])/TCP(flags="SA")
            print("connect to app")
            self.status = statuses[1]
            self.connect_to_server()
            self.status = statuses[2]
        except Exception as e:
            print(str(e))
            print("can't make a fully connection")


    def connect_to_server(self):
        target_addr = self.srv_addr[0]+','+str(self.srv_addr[1])
        self.serv_sock.connect(server_conn)
        self.serv_sock.sendall(b'p')
        msg = '41'+str(len(target_addr)).rjust(2,'0')+target_addr
        self.serv_sock.sendall(msg.encode())

    def connect_app(self, key):
        pass

    def run(self):
        print("my new sock with app-> " + self.app_sock_c)

if __name__ == '__main__':
    prx = Proxy(" ")