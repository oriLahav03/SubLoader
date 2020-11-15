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

    def make_auth(self):
        """
        docstring
        """
        while True:
            c = int(input('Welcome: \n1-singup\n2-login'))
            if c == 1:
                email = input("enter email: ")
                username = input("enter username: ")
                pw = input("enter password")
                con_pw = input("enter confirm passsword")
                self.sc.sendall(str('01'+email+'!'+username+'!'+pw+'!'+con_pw).encode())

                ret_c = self.sc.recv(2)
                ret_msg = self.sc.recv(128).decode().split('!')
                if(ret_msg[1] == 's'):
                    print('secccesful new user with email '+ret_msg[0])
                else:
                    print('unsecccesful new user\n'+ret_msg[0])
                    continue
            elif c == 2:
                email = input("enter email: ")
                username = input("enter username: ")
                self.sc.sendall(str('01'+email+'!'+pw).encode())

                ret = self.sc.recv(3).decode()
                if(ret[2]=='s'):
                    print('login secccesful')
                else:
                    print('login unsecccesful \nusername or password incorrect')
                    continue
            else:
                print('not an option')
                continue

            break
            
if __name__ == "__main__":
    clnt = Client()
    clnt.make_auth()
    start_new_thread(clnt.get_msg_thread,tuple())
    while True:
        try:
            if clnt.enter_n_send():
                break
        except Exception as e:
            print('main Error: '+ str(e))
            break 
    clnt.sc.close()
