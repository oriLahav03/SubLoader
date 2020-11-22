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
            isenter = clint.sc_lock.acquire()
            self.sc.send(str.encode(inp))
            clint.sc_lock.release()
        if inp == 'q':
            return True

    def get_msg_thread(self):
        while True:
            try:
                self.get_n_print()
            except:
                break
    
    def __do_singup(self ):
        email = input("enter email: ")
        username = input("enter username: ")
        pw = input("enter password: ")
        con_pw = input("enter confirm password: ")
        self.sc.sendall(str('01' + email + '!' + username + '!' + pw + '!' + con_pw).encode())

        ret_c = self.sc.recv(3).decode()
        if ret_c[2] == 's':
            ret_msg = self.sc.recv(128).decode().split('!')
            print('successful new user \nwith email ' + ret_msg[0] + ' and ip ' + ret_msg[1])

            self.vir_ip = ret_msg[1]
            self.networks = []
            self.un = ret_msg[0]
        else:
            print('unsuccessful new user\n' + self.sc.recv(128).decode())
            return True

    def __do_login(self):
        email = input("enter email: ")
        pw = input("enter password: ")
        self.sc.sendall(str('02' + email + '!' + pw).encode())

        ret_c = self.sc.recv(3).decode()
        if ret_c[2] == 's':
            print('login successful')
            s = int(self.sc.recv(3).decode())
            ret_msg = self.sc.recv(s).decode().split('!') 
            print('username: ' + ret_msg[0] + ' ip: ' + ret_msg[1] +'\nrooms: ' + ret_msg[2])

            self.vir_ip = ret_msg[1]
            self.networks = eval(ret_msg[2])
            self.un = ret_msg[0]
        else:
            print('login unsuccessful \nusername or password incorrect')
            return True

    def make_auth(self):
        """
        docstring
        """
        while True:
            c = int(input('Welcome: \n1-singup\n2-login\n'))
            if c == 1:
                if self.__do_singup():
                    continue
            elif c == 2:
                if self.__do_login():
                    continue
            else:
                print('not an option')
                continue

            break


if __name__ == "__main__":
    clint = Client()
    clint.make_auth()
    start_new_thread(clint.get_msg_thread, tuple())
    while True:
        try:
            if clint.enter_n_send():
                break
        except Exception as e:
            print('main Error: ' + str(e))
            break 
    clint.sc.close()
