from DB_helper import *
import pyrebase

HOST = '127.0.0.1'
PORT = 4000
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
# login ->  02name\email!password               #02s\f!(username!ip)\err
# delete user -> 03email!password               #03s\f

# new room -> 10size(3bytes)#roomname#roomadmin#password(optional)
    #settings{new_users : true\false, need_pass: true\false, accept_manual : true\false}
# join room -> 11roomname#password(if needed)
# leave room -> 12roomname (if he is the admin need to give it to other)
# change room admin -> 13roomname#user
# kick from room -> 14roomname#user
# delete room -> 15roomname
# change password -> 16roomname#newpassword
# change settings -> 17size(3bytes)settings{new_users : true\false, need_pass: true\false, accept_manual : true\false}


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

    def __get_userinfo_with_email(self, email):
        stats = catch_exception_get_db(self.db.child('Users').order_by_child('email').equal_to(email).get().val(),
                                       "ERROR: can't get the stats")
        if stats:
            return stats.popitem()
        else:  # TODO need to raise exception or something but for now...
            return False

    def singup(self, s_up: Singup):
        if s_up.password == s_up.conf_pw:
            try:
                new_user_data = self.auth.create_user_with_email_and_password(s_up.email,
                                                              s_up.password)  # Sign up with email and password
                print("User successfully created!")
            except Exception as e:
                print("ERROR: Wrong Email or Password input!")
                return False, str(e)

            ip_id, ip = get_free_ip(self.db)
            user_info = catch_exception_put_db(
                self.db.child("Users").child(s_up.email.split('@')[0]).set({'username': s_up.username, 'ip': ip,
                                                                            'email': s_up.email}),
                "ERROR: can't add new user")
            update_ip = catch_exception_put_db(self.db.child("IPS").child(ip_id).update({'used': True}),
                                               "ERROR: can't change parameter")
            return True, ip
        else:
            return False, "passwords not match!"

    def login(self, l_in: Login):
        # login auth section
        try:
            token = self.auth.sign_in_with_email_and_password(l_in.email,
                                                              l_in.password)  # Sign up with email and password
            print("User successfully logged in!")
        except Exception as e:
            print("ERROR: Wrong Email or Password input!")
            return False, str(e)
            # get user data section
        stat = self.__get_userinfo_with_email(l_in.email)
        return True, (
            stat[0], stat[1]['ip'], token['idToken'])  # if the action succeed and the user info (name,ip,token)

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
            stat = self.__get_userinfo_with_email(email)
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
        """
        get = self.db.child("Networks").order_by_key().equal_to(name).get()
        if 0 != len(get.pyres):
            return get.val()
        return False
        
    def add_new_room(self, room):
        """
        Add new room to the DB 
        """
        if self.__is_room_exists(room.name):
            #TODO raise taken_room_name
            pass
        room_data = {"password" : room.password, "admin" : room.admin, "users" : [],
            "settings" : {"new_users" : "true", "need_pass": room.need_password, "accept_manual" : "false"}}
        catch_exception_put_db(self.db.child("Networks").child(room.name).set(room_data), "error enter new room")

    def join_room(self, room_name, password, new_user_ip):
        """
        join to a new room 
        """
        val = self.__is_room_exists(room_name)
        if val:
            if val[room_name]['users'] == password:#or in settings need_pass is false
                user_list = val[room_name]['users']
                user_list.append(new_user_ip)
                is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                    {"users":user_list}), "can't add user "+ new_user_ip + " to room " + room_name)
            else:
                #TODO raise password_not_match
                pass
        else:
            #TODO raise room_not_exist
            pass

    def leave_room(self, room_name, user_ip):
        """
        removing aa user from a room
        """
        val = self.__is_room_exists(room_name)
        if val:
            user_list = val[room_name]['users']
            if user_ip in user_list:
                user_list.remove(user_ip)
                is_updated = catch_exception_put_db(self.db.child("Networks").child(room_name).update(
                        {"users":user_list}), "can't remove user "+ user_ip + " from room " + room_name)
        else:
            #TODO raise room_not_exist
            pass

if __name__ == '__main__':
    # tester
    gdb = Google_DB(database, authentication)
    gdb.leave_room('try', "anony")

