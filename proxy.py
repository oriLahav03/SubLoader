from vpn_manager import *
import random
from threading import *

proxy_addr = ("127.0.0.1", 1900)
src_ip = 0
dst_ip = 1
sock_indx = 0
lock_indx = 1
# protocols: first the server get 'p' msg then pass the connection to the proxy
#41size(2bytes)ip,port <= this addr belong to the target client -> server app
#                     fully new connect- need to open socket in other client
#42key(3byte) there is exeists Rout need to join it with the key
#get to_client addres 50size(2bytes)ip,port (comes after 41\2)
#
#tell client to make new app handling socket with server 60key(3byte)((2bytes)ip,port)=>maybe it works

class Rout(Thread):
    def __init__(self, from_sk, from_ad, to_clnt, client_list):
        super(Rout,self).__init__()
        self.f_sk=from_sk
        self.f_cln = self.__find_client(from_ad, client_list)
        self.t_cln = to_clnt

    def set_target_sk(self, sk, ad):
        """
        docstring
        """
        self.to_sk = sk
        self.to_ad = ad

    def set_key(self, k=0):
        self.key = k

    def __find_client(self, addr, clnts_l):
        for ad,cln in clnts_l:
            if cln.vir_ip == addr[0]:
                return cln
    def run(self):
        pass
        

class Proxy():
    """
    handle all the proxy connection from clients
    """
    def __init__(self, cln_list, lock):
        self.cln_l = cln_list
        self.cln_l_lk = lock
        self.rout_l = []

    def __check_key(self, k):
        """
        check if the key is free to use
        """
        if k != 0:
            for r in self.rout_l:
                if k == r.key:
                    return True
        return k == 0

    def new_conn(self, sock, addr):
        cod = int(sock.recv(2).encode())
        if cod == 41:
            key = 0
            while self.__check_key(int(key)):
                key = str(random.randint(1,999)).rjust(3,'0')
            target_clnt, target_addr = self.con_to_client(sock, key)
            new_rout = Rout(sock, addr, target_clnt, self.cln_l)
            new_rout.set_key(int(key))
            self.rout_l.append(new_rout)
        elif cod == 42:
            self.add_to_rout(sock, addr)


    def con_to_client(self, from_sock,key):
        """
        docstring
        """
        to_cln_addr = from_sock.recv(int(from_sock.recv(2).encode())).encode().split(',')
        for k,v in self.cln_l:
            if v.vir_ip == to_cln_addr[0]:
                target = v
                break
        target.sc.sendall(b'60'+key.encode())
        return target, to_cln_addr
        
    def add_to_rout(self, to_sock, to_ad):
        """
        docstring
        """
        key = int(to_sock.recv(3).decode())
        for r in self.rout_l:
            if r.key == key:
                r.set_target_sk(to_sock, to_ad)
                r.set_key()
                r.start()

class Gateway():
    def __init__(self):
        self.routing = {} # the virtual routing table via vir ips {ip:sock}
        self.rout_l = Lock()
        self.prx_sc = socket.socket()
        self.prx_sc.bind(proxy_addr)
        self.prx_sc.listen(10)

    def rout(self, v_ip , sock):
        """routing the traffic from one client to the right dst

        Args:
            v_ip (str): theirtual ip that need to add to the routing
            sock (socket): the proxy socket for the communication
        """
        sc_lock = Lock()
        self.rout_l.acquire()
        self.routing[v_ip] = (sock, sc_lock)
        self.rout_l.release()
        while True:
            #Get packet to send
            sc_lock.acquire()
            s = int(sock.recv(4).decode())
            headers, packet = sock.recv(s).decode().split(":", 1)
            headers = headers.split("-")
            sc_lock.release()
            #send the packet to the dst
            self.rout_l.acquire()
            self.routing[headers[dst_ip]][lock_indx].acquire()
            self.routing[headers[dst_ip]][sock_indx].sendall(packet.encode())
            self.routing[headers[dst_ip]][lock_indx].release()
            self.rout_l.release()
           

