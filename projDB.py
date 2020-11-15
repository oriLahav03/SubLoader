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
# singup- 01email!name!password!conf password #01s\femail\err msg!ip\none
# login-  02name\email!password               #02s\f(username!ip)\err


class Singup:
    def __init__(self, email, usrn, pw, conf):
        self.username = usrn
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

    def singup(self, s_up=Singup):
        if s_up.password == s_up.conf_pw:
            try:
                self.auth.create_user_with_email_and_password(s_up.email,
                                                              s_up.password)  # Sign up with email and password
                print("User successfully created!")
            except Exception as e:
                print("ERROR: Wrong Email or Password input!")
                return False, str(e)

            ip_id, ip = get_free_ip(self.db)
            user_info = catch_exception_put_db(
                self.db.child("Users").child(s_up.email.split('@')[0]).set({'username': s_up.username, 'ip': ip,
                                                                            'email': s_up.email}),
                'ERROR: cant add new user')
            update_ip = catch_exception_put_db(self.db.child("IPS").child(ip_id).update({'used': True}),
                                               'ERROR: cant change parameter')
            return True, ip
        else:
            return False, "passwords not match!"

    def login(self, l_in=Login):
        # login auth section
        try:
            token = self.auth.sign_in_with_email_and_password(l_in.email,
                                                              l_in.password)  # Sign up with email and password
            print("User successfully logged in!")
        except Exception as e:
            print("ERROR: Wrong Email or Password input!")
            return False, str(e)
            # get user data section
        stats = catch_exception_get_db(self.db.child('Users').order_by_child('email').equal_to(l_in.email).get().val(),
                                       'ERROR: cant get the stats')
        stat = stats.popitem()
        return True, (
            stat[0], stat[1]['ip'], token['idToken'])  # if the action succeed and the user info (name,ip,token)


if __name__ == '__main__':
    # tester
    ipsresulte = get_free_ip(database)
    print(ipsresulte)
    gdb = Google_DB(database, authentication)
    loginres = gdb.singup(Singup("ilay@gmail.com", 'gg', 'ilay120', 'ilay120'))
    print(loginres)
