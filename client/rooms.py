class Room_req():
    def __init__(self, clnt):
          self.clnt = clnt

    def new_room(self, name, paswrd, need_pass):
        room_data = '#'.join([name,self.clnt.vir_ip,paswrd,str(need_pass)])
        req = '10'+len(room_data)+room_data
        self.clnt.sc.send(req.encode())

        res = self.clnt.sc.rcev(512)
        return res[2:]