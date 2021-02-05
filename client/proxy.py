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

my_vir_ip = "25.200.0.10"
ips = ["25.200.0.10", "25.200.0.100"]

class Proxy():
    def __init__(self, data):
        self.gate_con = socket.socket()
        self.room_s_mems = data
        self.prv_addr = (get_if_hwaddr(conf.iface), get_if_addr(conf.iface))
        self.thrd_conn = []

    def pkt_routing(self, ifc=None): #thread
        print("start:")
        sniff(lfilter=self.out_routing, filter="tcp or icmp", prn=self.send_pkt_to_ga, iface=ifc)
        print("end!")
    
    def open_proxy_con(self):
        self.gate_con.connect((server_conn))
        self.gate_con.sendall(b'p')
        self.gate_con.sendall(str(len()))
        
    def out_routing(self, p):
        global my_vir_ip
        global ips
        return p[IP].dst in ips 


    def send_pkt_to_ga(self, p):
        """
        send the packet to the gateway (server)
        p: the packet from the sniff
        """
        p[ip].src = my_vir_ip
        # TODO encrypt the raw packet
        #protocol send to gateaway: 4_bytes_of_size src_vir_ip-dst_vir_ip:the bytes of encrypted packet
        raw_pkt = str(p).encode()
        headers = (p[IP].src+'-'+p[IP].dst+':').encode()
        size = str(len(headers+raw_pkt)).rjust(4,'0')
        vpn_p = size.encode()+headers+raw_pkt
        self.gate_con.sendall(vpn_p)

    def send_pkt_to_net(self, p_dt, ifc=None):
        """
        get a vpn packet take out the original packet and send it
        to the network
        p_dt: vpn packet wuth data of the origin packet
        ifc: specify the interface to send the packet
        """
        decry_p = p_dt # TODO decrpt the packet
        pkt = Ether(decry_p)
        pkt[Ether].dst = self.prv_addr[0]
        pkt[IP].dst = self.prv_addr[1]
        sendp(pkt,iface=ifc)

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