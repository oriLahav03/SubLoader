import socket
from _thread import *
from DB.projDB import *

host = '127.0.0.1'
port = 10000
address = []




class Server:
    def __init__(self,db):
        self.gdb=db #db
        self.ServerSocket = socket.socket() #main socket
        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
            exit()

        print('Waiting for a Connections...\n')
        self.ServerSocket.listen(5)

    def handel_singup(self, cln_sc, msg = list):
        s_up = Singup(msg[0],msg[1], msg[2], msg[3])
        res = self.gdb.singup(s_up)
        if(res[0]):
            cln_sc.sendall(('01!'+s_up.email+'!s').encode())
        else:
            cln_sc.sendall(('01!'+res[1]+'!f').encode())

    def accept_clients(self):
        """accept new client
        """
        self.cliets_list = []
        self.Thread_count = 0
        self.client_lock = allocate_lock()
        self.sock_lock = allocate_lock()
        while True:
            Client, address = self.ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client, address))
            print('Thread Number: ' + str(self.Thread_count))

    def send_to_all(self, from_cln, msg=str):
        """send the msg to the connected clients
        Args:
            from_cln (addr): who send the msg
            msg ([str], optional): the msg to send. Defaults to str.
        """
        for cln in self.cliets_list:
            if from_cln not in cln:
                self.sock_lock.acquire()
                cln[0].sendall(msg.encode())
                self.sock_lock.release()

    def threaded_client(self, sc, addr):
        try:
            sc.send(str.encode('Welcome to the Server\nsend ur name to chat (16 leters max)'))
            name = sc.recv(16).decode()
            sc.sendall(str.encode("Hi " + name + '\nu can chat now (enter q for exit)'))
            is_connected = True
        except :
            is_connected = False

        if is_connected:
            self.client_lock.acquire()
            self.cliets_list.append((sc,addr,name))
            self.Thread_count += 1
            self.client_lock.release()
            
            while True:
                try:
                    data = sc.recv(512).decode()
                    if not data or data == 'q':
                        break
                    msg = "->" + name + ': ' + data
                    self.client_lock.acquire()
                    self.send_to_all(addr,msg)
                    self.client_lock.release()
                except:
                    break
            print('client: "'+ name +'" disconected')
            self.send_to_all(addr, name +' logout')
            self.client_lock.acquire()
            self.Thread_count -= 1
            self.cliets_list.remove((sc,addr,name))
            self.client_lock.release()
            sc.close()

if __name__ == '__main__':
    srvr = Server(Google_DB(database, authentication))
    srvr.accept_clients()
