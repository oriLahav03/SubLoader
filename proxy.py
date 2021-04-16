from vpn_manager import *
import socket
import random
from threading import *

proxy_addr = ("127.0.0.1", 1900)
src_ip = 0
dst_ip = 1
sock_indx = 0
lock_indx = 1


# protocols: first the server get 'p' msg then pass the connection to the proxy
# 41size(2bytes)ip,port <= this addr belong to the target client -> server app
#                     fully new connect- need to open socket in other client
# 42key(3byte) there is exeists Rout need to join it with the key
# get to_client addres 50size(2bytes)ip,port (comes after 41\2)
#
# tell client to make new app handling socket with server 60key(3byte)((2bytes)ip,port)=>maybe it works

class Rout(Thread):
    def __init__(self, from_sk, from_ad, to_clnt, client_list):
        super(Rout, self).__init__()
        self.f_sk = from_sk
        self.f_cln = self.__find_client(from_ad, client_list)
        self.t_cln = to_clnt

    def set_target_sk(self, sk, ad):
        """
        The function set the target socket
        :param sk: the socket
        :param ad: the address
        :return: None
        """
        self.to_sk = sk
        self.to_ad = ad

    def set_key(self, k=0):
        """
        The function set the key
        :param k:
        :return: None
        """
        self.key = k

    def __find_client(self, addr, clnts_l):
        """
        The function find the client needed
        :param addr:
        :param clnts_l:
        :return:
        """
        for ad, cln in clnts_l:
            if cln.vir_ip == addr[0]:
                return cln

    def run(self):
        pass


class Proxy:
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
        """
        The function start new connection
        :param sock: the socket
        :param addr: the address
        :return: None
        """
        cod = int(sock.recv(2).encode())
        if cod == 41:
            key = 0
            while self.__check_key(int(key)):
                key = str(random.randint(1, 999)).rjust(3, '0')
            target_clnt, target_addr = self.con_to_client(sock, key)
            new_rout = Rout(sock, addr, target_clnt, self.cln_l)
            new_rout.set_key(int(key))
            self.rout_l.append(new_rout)
        elif cod == 42:
            self.add_to_rout(sock, addr)

    def con_to_client(self, from_sock, key):
        """
        we don't use the class
        :param from_sock:
        :param key:
        :return:
        """
        target = ''
        to_cln_addr = from_sock.recv(int(from_sock.recv(2).encode())).encode().split(',')
        for k, v in self.cln_l:
            if v.vir_ip == to_cln_addr[0]:
                target = v
                break
        try:
            target.sc.sendall(b'60' + key.encode())
        except Exception as e:
            print(e)
        return target, to_cln_addr

    def add_to_rout(self, to_sock, to_ad):
        """

        :param to_sock:
        :param to_ad:
        :return:
        """
        key = int(to_sock.recv(3).decode())
        for r in self.rout_l:
            if r.key == key:
                r.set_target_sk(to_sock, to_ad)
                r.set_key()
                r.start()


class Gateway:
    def __init__(self):
        self.routing = {}  # the virtual routing table via vir ips {ip:sock}
        self.rout_l = Lock()
        self.prx_sc = socket.socket()
        self.prx_sc.bind(proxy_addr)
        self.prx_sc.listen(10)

    def rout(self, sock):  # thread
        """routing the traffic from one client to the right dst

        Args:
            sock (socket): the proxy socket for the communication
        """
        sc_lock = Lock()
        v_ip = sock.recv(int(sock.recv(2).decode())).decode()
        self.rout_l.acquire()
        self.routing[v_ip] = (sock, sc_lock)
        self.rout_l.release()
        sock.settimeout(0.5)
        print("new for ip:", v_ip)
        while True:
            # sc_lock.acquire()
            try:
                # Get packet to send
                s = int(sock.recv(4).decode())
                headers, packet = sock.recv(s).decode().split(":", 1)
                headers = headers.split("-")
                # sc_lock.release()
            except socket.timeout:
                # didn't get any packet
                continue  # print("dont get packet")
            except socket.error as se:
                break
            else:
                # send the packet to the dst
                try:
                    self.rout_l.acquire()  # get into the routing lock
                    target = self.routing[headers[dst_ip]]
                    self.rout_l.release()
                except KeyError:  # user with that virtual ip not found
                    print(headers[dst_ip] + " virtual ip not found")
                    self.rout_l.release()
                else:
                    s = str(len(packet)).rjust(4, '0')
                    msg = s.encode() + packet.encode()
                    target[lock_indx].acquire()  # get into the socket lock
                    try:
                        target[sock_indx].sendall(msg)
                        print(headers[0], "->" + headers[1])
                    except socket.error as e:
                        print("can't reach target")
                    except Exception as e:
                        print(e)
                    target[lock_indx].release()
        # out
        self.rout_l.acquire()
        del self.routing[v_ip]
        self.rout_l.release()
