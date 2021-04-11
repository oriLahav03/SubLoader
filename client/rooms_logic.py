class Room_req:
    def __init__(self, c):
        self.clnt = c

    def new_room(self, name, paswrd, need_pass, vir_ip):
        """
        The function send the new room requests to the server
        :param name: The room name
        :param paswrd: the room password
        :param need_pass: the room need password or not? (bool)
        :param vir_ip: the virtual ip of the member
        :return: The answer from the server
        """
        room_data = '#'.join([name, vir_ip, paswrd, str(need_pass)])
        req = '10' + str(len(room_data)).rjust(3, '0') + room_data
        self.clnt.sendall(req.encode())

        res = self.clnt.recv(512).decode()
        return res[2:]

    def join_new_room(self, room_name, paswrd=' '):
        """
        The function send the join new room requests to the server
        :param room_name: the room name
        :param paswrd: the room password
        :return: The answer from the server
        """
        data = room_name + '#' + paswrd
        req = '11' + data
        self.clnt.sendall(req.encode())

        res = self.clnt.recv(512).decode()
        return res[2:]

    def leave_room(self, room_name):
        """
        The function send the leave room requests to the server
        :param room_name: the room name
        :return: The answer from the server
        """
        req = '12' + room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(128).decode()
        return res[2:]

    def get_room_data(self, room_name):
        """
        The function send the get room data requests to the server
        :param room_name: the room name
        :return: the room data + failed or not
        """
        req = '18' + room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(3).decode()
        if res[2] == 's':
            networks_data = {}
            s = int(self.clnt.recv(3).decode())
            data = self.clnt.recv(s).decode().split('#') + ['{}']
            networks_data[room_name] = [eval(i) for i in data[:2]]
        else:
            return 'f' + self.clnt.recv(128).decode()
        return 's', networks_data[room_name][0]

    def give_admin(self, room_name, user_ip):
        """
        The function send the set admin requests to the server
        :param room_name: the room name
        :param user_ip: the new user to be admin
        :return: The answer from the server
        """
        req = '13' + room_name + '#' + user_ip
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def kick_user(self, room_name, user_ip):
        """
        The function send the kick user requests to the server
        :param room_name: the room name
        :param user_ip: the user to kick
        :return: The answer from the server
        """
        req = '14' + room_name + '#' + user_ip
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def del_room(self, room_name):
        """
        The function send delete room requests to the server
        :param room_name: the room name
        :return: The answer from the server
        """
        req = '15' + room_name
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def change_paswrd(self, room_name, new_pas):
        """
        The function send the change password requests to the server
        :param room_name: the room name
        :param new_pas: the new password
        :return: The answer from the server
        """
        req = '16' + room_name + '#' + new_pas
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]

    def change_sets(self, new_users, need_pass, manual_accept):
        """
        The function send the change sets requests to the server
        :param new_users: the user to set
        :param need_pass: if the room need password
        :param manual_accept: if its gonna be manual accept or not
        :return: The answer from the server
        """
        sets = str({'new_users': new_users, 'need_pass': need_pass, 'accept_manual': manual_accept})
        req = '17' + str(len(sets)) + sets
        self.clnt.sendall(req.encode())
        res = self.clnt.recv(64).decode()
        return res[2:]
