import socket
from _thread import *

host = '127.0.0.1'
port = 10000

class Client:
    def __init__(self):
        self.sc = socket.socket()
        self.sc_lock = allocate_lock()
        print('try to connect..')
        try:
            self.sc.connect((host, port))
        except socket.error as e:
            print(str(e))
            exit(1)

    def get_n_print(self):
        self.sc_lock.acquire()
        Response = self.cs.recv(128)
        self.sc_lock.release()
        print(Response.decode())

    def enter_n_send(self):
        inp = Input()
        if inp:
            clnt.sc_lock.acquire()
            self.cs.send(str.encode(inp))
            clnt.sc_lock.release()

    def get_msg_thread(self):
        while True:
            try:
                self.get_n_print()
            except Exception as e:
                print(e)

if __name__ == "__main__":
    clnt = Client()
    clnt.get_n_print()
    clnt.enter_n_send()
    clnt.get_n_print()

    while True:
        try:
            clnt.enter_n_send()
        except Exception as e:
            print(e)
            break   
    clnt.sc.close()