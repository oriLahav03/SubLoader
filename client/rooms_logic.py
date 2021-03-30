class Room_req():
    def __init__(self, c):
        self.clnt = c

    def new_room(self, name, paswrd, need_pass, vir_ip):
        room_data = '#'.join([name,vir_ip,paswrd,str(need_pass)])
        req = '10'+str(len(room_data)).rjust(3,'0')+room_data
        self.clnt.sendall(req.encode())

        res = self.clnt.recv(512).decode()
        return res[2:]

    def join_new_room(self, room_name, paswrd=' '):
        data = room_name + '#' + paswrd
        req = '11'+data
        self.clnt.sendall(req.encode())

        res = self.clnt.recv(512).decode()
        return res[2:]

    def leave_room(self, room_name):
        req = '12'+room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(128).decode()
        return res[2:]

    def get_room_data(self, room_name):
        req = '18'+room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(3).decode()
        if res[2] == 's':
            s = int(self.clnt.recv(3).decode())
            data = self.clnt.recv(s).decode().split('#')+['{}']
            self.networks_data[room_name] = [eval(i) for i in data[:2]]
        else:
            return 'f' + self.clnt.recv(128).decode()
        return 's',self.networks_data[room_name]

    def give_admin(self, room_name, user_ip):
        req = '13'+room_name+'#'+user_ip
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def kick_user(self, room_name, user_ip):
        req = '14'+room_name+'#'+user_ip
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def del_room(self, room_name):
        req = '15'+room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def change_paswrd(self, room_name, new_pas):
        req = '16'+room_name+'#'+new_pas
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def change_sets(self, new_users, need_pass, manual_accept):
        sets = str({'new_users' : new_users, 'need_pass': need_pass, 'accept_manual' : manual_accept})
        req = '17'+len(sets)+sets
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]