class Room():
    """
    manage room info
    users: just virtual ip clients that in the room
    """
    def __init__(self, name, users, sets : dict):
        self.room_name = name
        self.users = users[:-1]
        self.sets = sets
        self.admin = users[-1]


class Client():
    """
    manage client info
    """
    def __init__(self, sc : socket.socket, addr, name, email, vir_ip, rooms: list, tkn = ''):
        self.sc = sc
        self.addr = addr
        self.rooms = rooms
        self.name = name
        self.email = email
        self.vir_ip = vir_ip
        self.tkn = tkn
        