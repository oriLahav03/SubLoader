import pyrebase
import socket


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

#protocols:
#singup- 01!name!password!email #01!email!s\f
#login-  02!name\email!password

class Connection:
    def __init__(self, db):
        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.g_db = db
        try:
            self.sc.connect((HOST,PORT))
        except Exception as e:
            print("Err connection server:\n" + e)
            exit(1)

    def get_request(self):
        msg = self.sc.recv(1024)
        msg = msg.split('!')
    
    def singup(self, msg = list):
        s_up = singup(msg[0],msg[1], msg[2])
        if(self.g_db.handel_singup(s_up)):
            self.sc.sendall(b('01!'+msg[1]+'!s').encode())
        else:
            self.sc.sendall(('01!'+msg[1]+'!f').encode())
        
class Singup:
    def __init__(self, usrn, pw, email):
        self.username = usrn
        self.password = pw
        self.email = email

class Login:
    def __init__(self, pw, email):
        self.password = pw
        self.email = email

class Google_DB:
    def __init__(self,db, auth):
        self.db = db
        self.auth = auth

    def handel_singup(self, s_up = Singup):
        try:
            self.auth.create_user_with_email_and_password(s_up.email, s_up.password)  # Sign up with email and password
            print("User successfully created!")
        except:
            print("Email already exists!")
            return False
        return True
    
    def handel_login(self, l_in):
        pass

if __name__ == '__main__':
    con = Connection(Google_DB(database, authentication))