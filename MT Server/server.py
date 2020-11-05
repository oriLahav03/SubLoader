import socket
from _thread import *


host = '127.0.0.1'
port = 10000
address = []




class Server:
    def __init__(self):
        self.ServerSocket = socket.socket()
        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print('Waiting for a Connections...\n')
        self.ServerSocket.listen(5)

    def accept_clients(self):
        self.cliets_list = []
        self.Thread_count = 0
        self.client_lock = allocate_lock()
        self.sock_lock = allocate_lock()
        while True:
            Client, address = self.ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client, address))
            
            print('Thread Number: ' + str(self.Thread_count))


    def threaded_client(self, sc, addr):
        sc.send(str.encode('Welcome to the Server\nsend ur name to chat (16 leters max)\n'))
        name = sc.recv(16).decode()

        self.client_lock.acquire()
        self.cliets_list += (sc,addr,name)
        self.Thread_count += 1
        self.client_lock.release()
        
        while True:
            try:
                data = sc.recv(512).decode()
                msg = "->" + name + ': ' + data
                self.client_lock.acquire()
                for cln in self.cliets_list:
                    if sc not in cln:
                        self.sock_lock.acquire()
                        cln[0].sendall(msg.encode())
                        self.sock_lock.release()
                self.client_lock.release()
            except:
                print('client disconected')
                break

            if not data:
                break
            try:
                #sc.sendall(str.encode(reply))
                pass
            except:
                break
        
        #print("\n", address[0] + ':' + str(address[1]), " disconnected", "\n")
        self.client_lock.acquire()
        self.Thread_count -= 1
        self.cliets_list.remove(sc,addr,name)
        self.client_lock.release()
        sc.close()



if __name__ == '__main__':
    srvr = Server()
    srvr.accept_clients()
