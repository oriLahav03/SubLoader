from DB_helper import *
import socket
import pyrebase

firebaseConfig = {'apiKey': "AIzaSyAsWlvXK-lblE2C9QWt8HNwKKCO6GsB26E",
                  'authDomain': "subloader-98331.firebaseapp.com",
                  'databaseURL': "https://subloader-98331.firebaseio.com",
                  'projectId': "subloader-98331",
                  'storageBucket': "subloader-98331.appspot.com",
                  'messagingSenderId': "763871684411",
                  'appId': "1:763871684411:web:6f8cca8650dfc178cb391e",
                  'measurementId': "G-2WBR7EQDYC"}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
authentication = firebase.auth()


# storage = firebase.storage()

# protocols:
# singup -> 01email!name!password!conf password #01s\f!email\err msg!ip\none
# login ->  02name\email!password               #02s\fsize(3bytes)(username!ip!rooms)\err
# delete user -> 03email!password               #03s\f

# new room -> 10size(3bytes)#roomname#roomadmin#password(optional)
    #need_pass: true\false                      #10s\f+err
# join room -> 11roomname#password(if needed)   #11s\f#room data\err
# leave room -> 12roomname (if he is the admin need to give it to other) #12s\f
# get rooms data -> 18roomname                  #18s\fsize(3bytes)["users ips"]#setting if admin({as dict})
#check if admin:
    # change room admin -> 13roomname#user      #13s\f
    # kick from room -> 14roomname#user         #14s\f need modify members
    # delete room -> 15roomname                 #15s\f need modify members
    # change password -> 16roomname#newpassword #16s\f
    # change settings -> 17size(3bytes)settings
    # {'new_users' : true\false, 'need_pass': true\false, 'accept_manual' : true\false}
                                                #17s\f


class Singup:
    def __init__(self, email, username, pw, conf):
        self.username = username
        self.password = pw
        self.email = email
        self.conf_pw = conf


class Login:
    def __init__(self, email, pw):
        self.password = pw
        self.email = email


class Google_DB:
    def __init__(self, db, auth):
        self.db = db
        self.auth = auth

    def get_free_ip(self):
        """
        the function give the first free to use ip from the database
        :return: the ip
        """
        ips = catch_exception_get_db(self.db.child('IPS').order_by_child('used').limit_to_first(1).get().val(),
                                    'ERROR: cant get ip...')
        ip = ips.popitem()
        if ip[1]['used'] is False:
            return ip[0], ip[1]['ip']
        else:
            raise get_ip_err()

    def __get_userinfo_by(self, child, eql):
        """get the wanted user by value that provide

        Args:
            child (the type of the value): which value of the DB we get
            eql (the value): a value of a user we want to get

        Raises:
            get_userinfo_err: if there is none user with that value

        Returns:
            [userinfo]: all the user information from the DB
        """
        stats = catch_exception_get_db(self.db.child('Users').order_by_child(child).equal_to(eql).get().val(),
                                       "ERROR: can't get the stats")
        if stats:
            return stats.popitem()
        else:  
            raise get_userinfo_err(child, eql)

    def __add_room_to_user_rooms(self, user, room_n):
        """add the new room the user connected to his room list

        Args:
            user (ip of the user): to find the user
            room_n (room name): the room name that the user joined
        """
        user_if = self.__get_userinfo_by('ip', user)
        try:
            user_rooms = user_if[1]['networks']
            user_rooms.append(room_n)
        except KeyError as e:
            user_rooms =[room_n]
        is_updated = catch_exception_put_db(self.db.child("Users").child(user_if[0]).update(
            {'networks': user_rooms}), "cant add room from list")

    def singup(self, s_up: Singup):
        """make singup new user

        Args:
            s_up (structure with info): all new user information

        Returns:
            [bool]: is succed
            if yes also the info we have else the error
        """
        if s_up.password == s_up.conf_pw:
            try:
                new_user_data = self.auth.create_user_with_email_and_password(s_up.email,
                                                                              s_up.password)  # Sign up with email and password
                print("User successfully created!")
            except Exception as e:
                print("ERROR: Wrong Email or Password input!")
                return False, str(e)

            ip_id, ip = self.get_free_ip()
            user_info = catch_exception_put_db(
                self.db.child("Users").child(s_up.username).set({'username': s_up.username, 'ip': ip,
                                                                            'email': s_up.email,'networks': []}),
                "ERROR: can't add new user")
            update_ip = catch_exception_put_db(self.db.child("IPS").child(ip_id).update({'used': True}),
                                               "ERROR: can't change parameter")
            return True, ip, new_user_data["localId"]
        else:
            return False, "passwords not match!"

    def login(self, l_in: Login):
        """login new client

        Args:
            l_in (structure with info): all new user informatio

        Returns:
            [bool]: is succed
            if yes also the info we have else the error
        """
        # login auth section
        try:
            token = self.auth.sign_in_with_email_and_password(l_in.email,
                                                              l_in.password)  # Sign up with email and password
            #print("User successfully logged in!")
        except Exception as e:
            #print("ERROR: Wrong Email or Password input!")
            return False, str(eval(e.strerror)['error']['message'])
        # get user data section
        stat = self.__get_userinfo_by('email', l_in.email)
        try:
            nets = stat[1]['networks']
        except KeyError as kerr:
            nets = []
        return True, (
            stat[1]['username'], stat[1]['ip'], nets ,token['localId'])  # if the action succeed and the user info (name,ip,token)

    def del_user(self, token, email):
        """
        the function handle all the user delete
        :param token: the user token
        :param email: the email of the user
        :return: None
        """
        try:
            self.auth.delete_user_account(token)
            flag = True
        except:
            print("can't delete user")
            flag = False

        if flag is True:
            stat = self.__get_userinfo_by('email', email)
            del_user_info = catch_exception_put_db(self.db.child('Users').child(stat[0]).set(None),
                                                   "ERROR: can't delete user")
            ips = catch_exception_get_db(
                self.db.child('IPS').order_by_child('ip').equal_to(stat[1]['ip']).get().val(),
                "ERROR: can't get ip")
            ip = ips.popitem()
            catch_exception_put_db(self.db.child('IPS').child(ip[0]).child('used').set(False),
                                   "ERROR: can't change ip to not used")
            print("User successfully deleted!")

    def __is_room_exists(self, name):
        """
        checking if the room exists by name
        if yes return it else return false

        Args:
            name : the name of the room
        """
        get = self.db.child("Networks").order_by_key().equal_to(name).get()
        # tget = self.db.child("Networks").child(name).get().val()['users'] after can give up on room_name var
        if 0 != len(get.pyres):
            return get.val()
        return False

    def __can_join_new_room(self, room_val, password):
        """check if new user can join the room
            pass match \ not accept new \
        Args:
            room_val ([room from db]): [description]
            new_user_ip ([ip of user]): wo wants to join
            password (str): [password for room].
        """
        if room_val['settings']['new_users']:
            if room_val['pass'] == password or not room_val['settings']['need_pass']:
                return True
            else:
                raise password_not_match(password, room_val)
        else:
            return False

    def is_room_admin(self, room_name, user_ip):
        """check if the user is the admin of the room

        Args:
            room_name (str): name of the room
            user_ip (str): the user virtual ip

        Raises:
            room_not_exist: not find a room with that name

        Returns:
            [bool]: [if admin or not]
        """
        val = self.__is_room_exists(room_name)
        if val:
            if user_ip == val[room_name]['admin']:
                return True
            else:
                return False
        else:
            raise room_not_exist(room_name, 'can\'t find room ')

    def add_new_room(self, room):
        """Add new room to the DB 

        Args:
            room (str): room name

        Raises:
            name_taken: if room already exists
        """
        if self.__is_room_exists(room.name):
            raise name_taken(room.name, 'room')
        room_data = {"pass": room.password, "admin": room.admin, "users": [],
                     "settings": {"new_users": "True", "need_pass": room.need_password, "accept_manual": "False"}}
        catch_exception_put_db(self.db.child("Networks").child(room.name).set(room_data), "error enter new room")
        self.__add_room_to_user_rooms(room.admin, room.name)

    def join_room(self, room_name, new_user_ip, password=''):
        """join to a new room 

        Args:
            room_name (str): room name
            new_user_ip (str): the ip of the new user that joined
            password (str, optional): password of the room. Defaults to ''.

        Raises:
            join_room_err: cant join room error
            room_not_exist: not find a room with that name
        """
        val = self.__is_room_exists(room_name)
        if val:
            if self.__can_join_new_room(val[room_name], password):
                try:
                    user_list = val[room_name]['users']
                    user_list.append(new_user_ip)
                except KeyError as e:
                    user_list = [new_user_ip]
                is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                    {"users": user_list}), "can't add user " + new_user_ip + " to room " + room_name)
                
                self.__add_room_to_user_rooms(new_user_ip, room_name)
            else:
                raise join_room_err(room_name)
        else:
            raise room_not_exist(room_name)

    def remove_from_room(self, room_name, user_ip):
        """removing a user from a room
        and the room name from his list

        Args:
            room_name (str): room to remove the user from
            user_ip (str): virtual ip of the user

        Raises:
            room_not_exist: if room not exists
        """
        val = self.__is_room_exists(room_name)
        if val:
            user_list = val[room_name]['users']
            if user_ip in user_list:
                user_list.remove(user_ip)
                is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                    {"users": user_list}), "can't remove user " + user_ip + " from room " + room_name)

                user_if = self.__get_userinfo_by('ip', user_ip)
                user_rooms = user_if[1]['rooms']
                user_rooms.remove(room_name)
                is_updated = catch_exception_put_db(self.db.child("Users").child(user_if[0]).update(
                    {'rooms': user_rooms}), "cant remove room from list")
        else:
            raise room_not_exist(room_name)
            
    def change_room_pass(self, room_name, new_pass):
        """change password for room

        Args:
            room_name (str):
            new_pass (str): new password for the room

        Raises:
            room_not_exist: cant find room error
        """
        val = self.__is_room_exists(room_name)
        if val:
            is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                {"pass": new_pass}), "can't update password for room " + room_name)
        else:
            raise room_not_exist(room_name)

    def change_sets(self, room_name, sets):
        """change settins for the room

        Args:
            room_name (str): room name
            sets (str(dict)): the dict of the settings in str

        Raises:
            room_not_exist: cant find room error
        """
        val = self.__is_room_exists(room_name)
        if val:
            is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                    {'settings' : eval(sets)}), "can't update settings")
        else:
            raise room_not_exist(room_name)
    
    def del_room(self, room_name):
        """delete room

        Args:
            room_name (str): room to delte

        Raises:
            room_not_exist: cant find room error
        """
        val = self.__is_room_exists(room_name)
        if val:
            user_list = val[room_name]['users'] + [val[room_name]['admin']]
            for usr_ip in user_list:
                user_if = self.__get_userinfo_by('ip', usr_ip)
                user_rooms = user_if[1]['rooms']
                user_rooms.remove(room_name)
                is_updated = catch_exception_put_db(self.db.child("Users").child(user_if[0]).update(
                    {'rooms': user_rooms}), "cant remove room from list")
            self.db.child("Networks").child(room_name).remove()
        else:
            raise room_not_exist(room_name)

    def change_admin(self,name, ip):
        """change admin of the room

        Args:
            name (str): room name
            ip (str): ip of the new admin

        Raises:
            room_not_exist: cant find room error
        """
        val = self.__is_room_exists(name)
        if val:
            user_list = val[name]['users']
            if ip in user_list:
                user_list.remove(ip)
                user_list.append(val[name]['admin'])
            is_updated = catch_exception_put_db(self.db.child("Users").child(name).update(
                    {'admin' : ip, 'users' : user_list}), "cant update admin")
        else:
            raise room_not_exist(name)

    def get_room_data(self, room_name, vir_ip):
        """
         get the room data
        Raises:
            room_not_exist: [if room in this name not founde]

        Returns:
            [list]: [list of users in ]
            [dict]: [the settings of the network, only give to admin]
        """
        val = self.__is_room_exists(room_name)
        if val:
            user_list = []
            try:
                user_list += val[room_name]['users'] 
            except KeyError as e:
                pass
            finally:
                user_list += [val[room_name]['admin']]
            sets = val[room_name]['settings']
            if vir_ip not in user_list:
                raise get_data_err('room', room_name, 'can\'t find room')
            return user_list, sets
        else:
            raise room_not_exist(room_name)
            

class NewRoom:
    def __init__(self, data: list):
        self.name = data[0]
        self.admin = data[1]
        self.password = data[2]
        self.need_password = data[3]


class Room_manager:
    def __init__(self, db: Google_DB):
        self.db = db

    def __get_data_with_size(self, sc: socket.socket):
        """return data from socket

        Args:
            sc (socket): user socket for data

        Returns:
            list: list of the parametrs
        """
        size = int(sc.recv(3).decode())
        req_msg = sc.recv(size).decode()
        data = req_msg.split('#')
        return data

    def __get_data(self, sc: socket.socket):
        """return data from socket

        Args:
            sc (socket): user socket for data

        Returns:
            list: list of the parametrs
        """
        req_msg = sc.recv(1024).decode()
        data = req_msg.split('#')
        return data

    def __new_room(self, data: list):
        """acomplish new room request

        Args:
            data (list): parametrs to work with

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.add_new_room(NewRoom(data))
            return 's'
        except name_taken as e:
            return 'f' + str(e)

    def __join_room(self, data: list, vir_ip):
        """acomplish join to new room

        Args:
            data (list): parameters
            vir_ip (str): virtual ip of the user

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.join_room(data[0], vir_ip, data[1])
            return 's'
        except join_room_err as e:
            return 'f' + str(e)

    def __leave_room(self, data: list, vir_ip):
        """make leave room operation

        Args:
            data (list): the data to work with
            vir_ip (str): virtual ip of the user

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.remove_from_room(data[0], vir_ip)
            return 's'
        except room_not_exist as e:
            return 'f' + str(e)

    def __change_admin_in_room(self, data: list):
        """change admin of room

        Args:
            data (list): the data

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.change_admin(data[0], data[1])
            return 's'
        except Exception as e:  # TODO: add exception
            return 'f' + str(e)

    def __kick_from_room(self, data: list):
        """kick user from room

        Args:
            data (list): the data to work with

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.remove_from_room(data[0], data[1])
            return 's'
        except room_not_exist as e:
            return 'f' + str(e)

    def __delete_room(self, data: list):
        """delete the room

        Args:
            data (list): the data

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.del_room(data[0])
            return 's'
        except room_not_exist as e:
            return 'f' + str(e)

    def __change_password(self, data: list):
        """change password for room

        Args:
            data (list): data to work with

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.change_room_pass(data[0], data[1])
            return 's'
        except room_not_exist as e:
            return 'f' + str(e)

    def __change_settings(self, data: list):
        """change room settings

        Args:
            data (list): the data

        Returns:
            str: msg to client if the operation worked
        """
        try:
            self.db.change_sets(data[0], data[1])
            return 's'
        except room_not_exist as e:
            return 'f' + str(e)

    def __give_room_data(self, data: list, vir_ip):
        """
        get room data from db and send

        Returns:
            [str]: if succed and the data of the room
        """
        print('give room %s from db' % (data[0]))
        print(data)
        try:
            users, sets = self.db.get_room_data(data[0], vir_ip)
            msg = str(users)+ '#' +str(sets)
            print(msg)
            size = len(msg)
            return 's'+ str(size).rjust(3,'0') + msg
        except get_data_err as e:
            return 'f'+str(e)
        except room_not_exist as e:
            return 'f' + str(e)

    def handle_request(self, clnt):
        """handle all the request from a client

        Args:
            clnt (struct): client parametrs and information
        """
        code = clnt.sc.recv(2).decode()  # msg code
        if code == '10':
            data = self.__get_data_with_size(clnt.sc)
            clnt.sc.send('10'.encode() + self.__new_room(data).encode())
        elif code == '11':
            data = self.__get_data(clnt.sc)
            clnt.sc.send('11'.encode() + self.__join_room(data, clnt.vir_ip).encode())
        elif code == '12':  # TODO: give the admin to another if admin leave
            clnt.sc.send('12'.encode() + self.__leave_room(data, clnt.vir_ip).encode())
        elif code == '18':
            data = self.__get_data(clnt.sc)
            clnt.sc.send('18'.encode() + self.__give_room_data(data, clnt.vir_ip).encode())
        elif code != '17':
            data = self.__get_data(clnt.sc)
            if self.db.is_room_admin(data[0], clnt.vir_ip):
                if code == '13':
                    clnt.sc.send('13'.encode() + self.__change_admin_in_room(data).encode())
                elif code == '14':
                    clnt.sc.send('14'.encode() + self.__kick_from_room(data).encode())
                elif code == '15':
                    clnt.sc.send('15'.encode() + self.__delete_room(data).encode())
                elif code == '16':
                    clnt.sc.send('16'.encode() + self.__change_password(data).encode())
            else:
                clnt.sc.send(code.encode() + 'fYou are not an admin'.encode())
        elif code == '17':
            data = self.__get_data_with_size(clnt.sc)
            clnt.sc.send('17'.encode() + self.__change_settings(data).encode())
        else:
            clnt.sc.send('00finvalid code'.encode())


if __name__ == '__main__':
    # tester
    gdb = Google_DB(database, authentication)
    # gdb.login(Login('ilay@gmail.com', 'ilay120'))
    gdb.del_room('try')
    # gdb.change_sets('try', '''{'new_users' : True, 'need_pass': False, 'accept_manual' : True}''')
