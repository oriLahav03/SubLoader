class Room_req():
    def __init__(self, clnt):
          self.clnt = clnt

    def new_room(self, name, paswrd, need_pass):
        room_data = '#'.join([name,self.clnt.vir_ip,paswrd,str(need_pass)])
        req = '10'+len(room_data)+room_data
        self.clnt.sc.send(req.encode())

        res = self.clnt.sc.rcev(512)
        return res[2:]

    def join_new_room(self, room_name, paswrd=' '):
        data = room_name + '#' + paswrd
        req = '11'+data
        self.clnt.sc.send(req.encode())

        res = self.clnt.sc.rcev(512)
        return res[2:]

    def leave_room(self, room_name):
        req = '12'+room_name
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(128)
        return res[2:]

    def get_room_data(self, room_name):
        req = '18'+room_name
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(128)
        return res[2:]

    def give_admin(self, room_name, user_ip):
        req = '13'+room_name+'#'+user_ip
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(64)
        return res[2:]

    def kick_user(self, room_name, user_ip):
        req = '14'+room_name+'#'+user_ip
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(64)
        return res[2:]

    def del_room(self, room_name):
        req = '15'+room_name
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(64)
        return res[2:]

    def change_paswrd(self, room_name, new_pas):
        req = '16'+room_name+'#'+new_pas
        self.clnt.sc.send(req.encode())
        res = self.clnt.sc.rcev(64)
        return res[2:]