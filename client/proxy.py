from scapy.all import *
from threading import Thread
import socket

statuses = {
    0:"need to accept",
    1:"connect accepted",
    2:"1+server conn",
    3:"only server conn"
}
server_conn = ("ec2-52-210-76-129.eu-west-1.compute.amazonaws.com",10000)

my_vir_ip = "25.200.0.10"
ips = ["25.200.0.11", "25.200.0.100","25.200.0.10"]

class Proxy():
    def __init__(self, my_vir_ip, rooms_mems):
        self.my_vir_ip = my_vir_ip
        self.ips = rooms_mems
        self.gate_con = socket.socket()
        self.sc_lock = Lock()
        self.room_s_mems = data
        self.prv_addr = (get_if_hwaddr(conf.iface), get_if_addr(conf.iface), self.get_router_mac())
        self.thrd_l = [Thread(target=self.open_proxy_con, args=(my_vir_ip,)),Thread(target=self.pkt_routing, args=(None,))]

    def get_router_mac(self):
        net_data = conf.route.route("0.0.0.0")
        try:
            res, un = sr(ARP(op="who-has", psrc=net_data[1], pdst=net_data[2]), timeout=100)
        except TimeoutError:
            return None
        return res[0][1][ARP].hwsrc

    def arp_res(self,arp_p):
        p = Ether(src="ac:f5:5a:b3:82:d5", dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=arp_p.psrc, psrc=arp_p.pdst, hwsrc="ac:f5:5a:b3:82:d5",op="is-at")
        srp1(p, iface="SubNet",verbose= False)


    def open_proxy_con(self, my_vir_ip):
        self.gate_con.connect((server_conn))
        open_msg = b'p' + str(len(my_vir_ip)).encode() +my_vir_ip.encode()
        self.gate_con.sendall(open_msg)
        #start recive routed packets from server
        while True:
            try:
                size = int(self.gate_con.recv(4).decode())
                pkt = self.gate_con.recv(size).decode()
                self.send_pkt_to_net(pkt)
            except Exception:
                break
            
        
    def pkt_routing(self, ifc=conf.iface): #thread
        print("start:")
        sniff(lfilter=self.out_routing, filter="tcp or icmp or arp", prn=self.send_pkt_to_ga, iface=ifc)
        print("end!")
    
    def out_routing(self, p):
        global my_vir_ip
        global ips
        if IP in p:
            return p[IP].dst in ips
        if ARP in p and p[ARP].op == "who-has":
            self.arp_res(p[ARP])
        return False 

    def send_pkt_to_ga(self, p):
        """
        send the packet to the gateway (server)
        p: the packet from the sniff
        """
        p[IP].src = my_vir_ip
        # TODO encrypt the raw packet
        # p = encrypt_func(str(p)) return str of encrypted packet
        #protocol send to gateaway: 4_bytes_of_size src_vir_ip-dst_vir_ip:the bytes of encrypted packet
        raw_pkt = str(p).encode()
        headers = (p[IP].src+'-'+p[IP].dst+':').encode()
        size = str(len(headers+raw_pkt)).rjust(4,'0')
        vpn_p = size.encode()+headers+raw_pkt
        print("catch packet to: "+p[IP].dst)
        print(p.summary())
        try:
            self.gate_con.sendall(vpn_p)
        except:
            exit()

    def send_pkt_to_net(self, p_dt, ifc=conf.iface):
        """
        get a vpn packet take out the original packet and send it
        to the network
        p_dt: vpn packet with data of the origin packet
        ifc: specify the interface to send the packet (None for no specify)
        """
        decry_p = p_dt # TODO decrpt the packet
        pkt = Ether(eval(decry_p))
        print("get packet from: "+pkt[IP].src)
        print("before",pkt.summary())
        pkt[Ether].dst = self.prv_addr[0]
        pkt[IP].dst = self.prv_addr[1]
        print("after", pkt.show())
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
    
    def start_threads(self):
        for t in self.thrd_l:
            t.start()



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
    prx = Proxy(my_vir_ip, ips)
    prx.start_threads()
    