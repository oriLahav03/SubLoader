class Client():
    """
    manage client info
    """
    def __init__(self, sc : socket.socket, addr, name, email, vir_ip, rooms):
        self.sc = sc
        self. addr = addr
        self.rooms = rooms
        self.name = name
        self.email = email
        self.vir_ip = vir_ip

class Room():
    """
    manage room info
    users: just virtual ip clients that in the room
    """
    def __init__(self, name, users):
        self.room_name = name
        self.users = users