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
            exit()

    def get_n_print(self):
        Response = ''
        self.sc_lock.acquire()
        try:
            self.sc.settimeout(0.1)
            Response = self.sc.recv(128)
        except socket.timeout:
            pass
        self.sc_lock.release()
        if Response:
            print(Response.decode())

    def enter_n_send(self):
        inp = input()
        if inp:
            isenter = clnt.sc_lock.acquire()
            self.sc.send(str.encode(inp))
            clnt.sc_lock.release()
        if inp == 'q':
            return True

    def get_msg_thread(self):
        while True:
            try:
                self.get_n_print()
            except Exception as e:
                break
                #print('thread Error: '+ str(e))

if __name__ == "__main__":
    clnt = Client()
    clnt.get_n_print()
    clnt.enter_n_send()
    clnt.get_n_print()
    start_new_thread(clnt.get_msg_thread,tuple())
    while True:
        try:
            if clnt.enter_n_send():
                break
        except Exception as e:
            print('main Error: '+ str(e))
            break 
    clnt.sc.close()