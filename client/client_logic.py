import socket
from _thread import *
from client_err import *
from rooms import *
import re

host = '127.0.0.1'
port = 10000

# Email must be in a some@some.com format
email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

# Password must contain:
# At list 1 Uppercase letter
# At list 1 number
# At list 6 chars
password_regex = r'[A-Za-z0-9]{6,20}'
username_regex = "\W"

class Client_logic:
    def __init__(self):
        self.vir_ip = ''
        self.my_networks= []
        self.networks_data = {}
        self.un = ''

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
    
    def __check_mail(self, eml):
        if not re.search(email_regex, eml):
           raise email_err("need to be @ and text in both side with a . in end", eml)

    def __check_password(self, pw):
        if not re.fullmatch(password_regex, pw):
            raise pw_err("at list 6 leter uper lower and numbers", pw)

    def __check_un(self, un):
        if re.findall(username_regex, un):
            raise un_err("only numbers leters and '_' alowed", un)
        if len(un) < 4 or len(un) > 18 :
            raise un_err("username size between 4 to 18", un)

    def __get_rooms_data(self):
        """get the rooms data from server

        Raises:
            get_data_err: [if fails geting data from some rooms]
        """
        err_rooms = []
        
        for room in self.my_networks:
            self.sc.sendall(str('18' + room).encode())
            res = self.sc.recv(3).decode()
            if res[2] == 's':
                s = int(self.sc.recv(3).decode())
                data = self.sc.recv(s).decode().split('#')+['']
                self.networks_data[room] = data[:2]
            else:
                err_rooms+=room
        if len(err_rooms):
            raise get_data_err('rooms', err_rooms)



    def do_singup(self, email = '', username = '', pw = '', con_pw = ''):
        """get data for new users

        Returns:
            [bool]: [true for unssucceful singup]
        """
        #if rais nothing its good
        self.__check_mail(email)
        self.__check_password(pw)
        self.__check_un(username)
        self.sc.sendall(str('01' + email + '!' + username + '!' + pw + '!' + con_pw).encode())

        ret_c = self.sc.recv(3).decode()
        if ret_c[2] == 's':
            ret_msg = self.sc.recv(128).decode().split('!')
            print('successful new user \nwith email ' + ret_msg[0] + ' and ip ' + ret_msg[1])

            self.vir_ip = ret_msg[1]
            self.un = username
            self.mail = ret_msg[0]
        else:
            print('unsuccessful new user\n' + self.sc.recv(128).decode())
            return True

    def do_login(self, email = '', pw = ''):
        """get data to make login

        Returns:
            [bool]: [true for unssucceful login]
        """
        #if rais nothing its good
        self.__check_mail(email)
        self.__check_password(pw)
        self.sc.sendall(str('02' + email + '!' + pw).encode())

        ret_c = self.sc.recv(3).decode()
        if ret_c[2] == 's':
            print('login successful')
            s = int(self.sc.recv(3).decode())
            ret_msg = self.sc.recv(s).decode().split('!') 
            print('username: ' + ret_msg[0] + ' ip: ' + ret_msg[1] +'\nrooms: ' + ret_msg[2])

            self.vir_ip = ret_msg[1]
            self.my_networks = eval(ret_msg[2])
            self.un = ret_msg[0]
            self.__get_rooms_data()
        else:
            print(self.sc.recv(128).decode())
            return True

    def make_auth(self):
        """try connect to the server and get the user data from it
        """
        while True:
            c = int(input('Welcome: \n1-singup\n2-login\n'))
            if c == 1:
                if self.__do_singup():
                    continue
            elif c == 2:
                if self.__do_login():
                    continue
                self.__get_rooms_data()
            else:
                print('not an option')
                continue
            break
    
    def init_room_req(self):
        self.room_req = Room_req(self.sc)

if __name__ == "__main__":
    clint = Client_logic()
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
