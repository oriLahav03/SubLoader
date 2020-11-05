import socket
from _thread import *

host = '127.0.0.1'
port = 10000

class Client:
    def __init__(self):
        self.sc = socket.socket()
        print('try to connect..')
        try:
            self.sc.connect((host, port))
        except socket.error as e:
            print(str(e))
            exit(1)

    def get_n_print(self):
        Response = self.cs.recv(512)
        print(Response.decode())
        
    def enter_n_send(self):
        inp = Input()
        self.cs.send(str.encode(inp))





if __name__ == "__main__":
    clnt = Client()
    clnt.get_n_print()
    clnt.enter_n_send()
    clnt.get_n_print()

    while True:
        Input = input('Say Something (to disconnect write "quit"): ')
        ClientSocket.send(str.encode(Input))
        if Input.lower() == 'quit':
            break
        Response = ClientSocket.recv(1024)
        print(Response.decode('utf-8'))

    ClientSocket.close()