from scapy.all import *
import socket

statuses = {
    0:"need to accept",
    1:"connect accepted",
    2:"1+server conn",
    3:"only server conn"
}
server_conn = ("127.0.0.1",10000)

my_vir_ip = "127.0.0.1"
ips = ["127.0.0.1", "168.192.1.1", "168.192.1.5", "25.200.2.86"]

class Proxy():
    def __init__(self, data):
        self.cln_dt = data
        self.thrd_conn = []
        print("start:")
        sniff(lfilter=self.routing, prn=self.prnt)
        print("end!")

    def routing(self, p):
        global my_vir_ip
        global ips
        if IP in p:
            return p[IP].dst in ips or p[IP].dst == my_vir_ip
        else:
            return False

    def port_taken(self, port):
        for c in self.thrd_conn:
            if port == c.my_addr[1]:
                return True
        return False

    def prnt(self, p):
        print(p.summary())
        print("send to => " + p[IP].dst)
        if not self.port_taken(p[TCP].dport):
            self.thrd_conn.append(ThirdPartyConnection(("0.0.0.0", p[TCP].dport)))#(p[IP].src, p[TCP].sport)




class ThirdPartyConnection():
    """
    new socket with the server
    and one with the third party applicatin
    make communication between them
    """
    def __init__(self, app_conn):
        self.app_sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_addr = app_conn
        self.app_sock_s.bind(app_conn)
        self.app_sock_s.listen()
        self.status = statuses[0]
        self.accespt_app()

    def accespt_app(self):
        try:
            self.app_sock_c, self.app_addr = self.app_sock_s.accept()
            self.status = statuses[1]
            self.connect_to_server()
            self.status = statuses[2]
        except Exception as e:
            print(str(e))
            print("can't make a fully connection")


    def connect_to_server(self):
        self.serv_sock.connect(server_conn)


if __name__ == '__main__':
    prx = Proxy(" ")
    


"""class temp(object):
    def __init__(self, g):
        self.name = "name"
        self.age = g
    
    def __eq__(self, o):
        return self.age == o.age

tlist = [temp(6),temp(77),temp(45)]"""