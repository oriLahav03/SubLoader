import socket
from _thread import *
from projDB import *
from vpn_manager import *

host = '127.0.0.1'
port = 10000


class Server:
    def __init__(self, db: Google_DB):
        self.sock_lock = allocate_lock()
        self.client_lock = allocate_lock()
        self.Thread_count = 0
        self.clients_list = {}
        self.gdb = db  # db
        self.ServerSocket = socket.socket()  # main socket
        try:
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
            exit()

        print('Waiting for a Connections...\n')
        self.ServerSocket.listen(5)

    def handle_singup(self, cln_sc, req: list):
        """
        handle singup request from client get the data from socket and send to db class.
        :param cln_sc: client socket to send results.
        :param req: list of parameters from socket, Defaults to list.
        :return: T for succeed F for fail.
        """
        s_up = Singup(req[0], req[1], req[2], req[3])
        res = self.gdb.singup(s_up)
        if res[0]:
            cln_sc.sendall(('01s' + s_up.email+ '!' + res[1]).encode())
            return False,(s_up.email,s_up.username,res[1],[], res[2])
        else:
            cln_sc.sendall(('01f' + res[1]).encode())
            return True,0

    def handle_login(self, cln_sc, req: list):
        """
        handle login request from client get the data from socket and send to db class.
        :param cln_sc: client socket to send results.
        :param req: list of parameters from socket, Defaults to list.
        :return: T for succeed F for fail.
        """
        l_in = Login(req[0], req[1])
        res = self.gdb.login(l_in)
        if res[0]:
            user_info = res[1][0] + '!' + res[1][1] +'!'+ str(res[1][2])
            cln_sc.sendall(('02s'+ str(len(user_info)).rjust(3,'0') + user_info).encode())
            return False,(l_in.email, res[1][0], res[1][1], res[1][2],res[1][0])
        else:
            cln_sc.sendall(('02f' + res[1]).encode())
            return True,0

    def new_auth(self, sc: socket.socket):
        """
        handle new client that want to enter the server.
        :param sc: client socket.
        :return: user info.
        """
        req_msg = 0
        out = [True,0]
        while out[0]:
            code = sc.recv(2).decode()
            req_msg = sc.recv(256).decode()
            req = req_msg.split('!')
            if int(code) == 1:
                out = self.handle_singup(sc, req)
            elif int(code) == 2:
                out = self.handle_login(sc, req)
            else:
                sc.send(b'00unknown code')
        return req[1]

    def accept_clients(self):
        """
        accept clients.
        :return: None.
        """
        while True:
            Client, address = self.ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            con_type = Client.recv(1).decode()
            if con_type == 'a':              #a for our app connection p to a proxy connection
                start_new_thread(self.threaded_client, (Client, address))
            elif con_type == 'p':
                start_new_thread(self.proxy.new_con, (Client, address))
            else:
                Client.sendall(b'00not chose type of connection')
                Client.close()
            print('Thread Number: ' + str(self.Thread_count))

    def send_to_all(self, from_cln, msg: str):
        """
        send the msg to the connected clients.
        :param from_cln: who send the msg.
        :param msg: the msg to send, Defaults to str.
        :return: None.
        """
        for cln in self.clients_list:
            if from_cln not in cln:
                self.sock_lock.acquire()
                cln[0].sendall(msg.encode())
                self.sock_lock.release()

    def threaded_client(self, sc, address):
        """
        the function talk with clients.
        :param sc: the client socket.
        :param address: the client address.
        :return: None.
        """
        try:
            usr_data = self.new_auth(sc)
            is_connected = True
        except Exception as e:
            print(str(e))
            is_connected = False

        if is_connected:
            self.client_lock.acquire()
            self.clients_list[(sc, address)] = Client(sc, address, usr_data[1], usr_data[0],usr_data[2],usr_data[3], usr_data[4])
            self.Thread_count += 1
            self.client_lock.release()

            while True:
                try:
                    data = sc.recv(512).decode()
                    if not data or data == 'q':
                        break
                    msg = "->" + name + ': ' + data
                    self.client_lock.acquire()
                    self.send_to_all(address, msg)
                    self.client_lock.release()
                except:
                    break
            print('client: "' + name + '" disconnected')
            self.send_to_all(address, name + ' logout')
            self.client_lock.acquire()
            self.Thread_count -= 1
            del self.clients_list[(sc, address)] # remove client
            self.client_lock.release()
            sc.close()


if __name__ == '__main__':
    server = Server(Google_DB(database, authentication))
    server.accept_clients()
