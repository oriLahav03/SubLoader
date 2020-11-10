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
db = firebase.database()
auth = firebase.auth()


def get_free_ip():
    ips = None
    try:
        ips = db.child('IPS').order_by_child('used').limit_to_first(1).get().val()
    except:
        print('ERROR: cant get ip...')
    for name, ip in ips.items():
        if ip['used'] is False:
            return name, ip
        else:
            return 'no'

      
def signup(username, email, password, confirm_password):
    if password == confirm_password:
        try:
            auth.create_user_with_email_and_password(email, password)  # Sign up with email and password
            print("User successfully created!")
            flag = True
        except:
            print("ERROR: Wrong Email or Password input!")
            flag = False
        if flag is True:
            ip_id, ip = get_free_ip()
            try:
                db.child("Users").child(email.split('@')[0]).set({'username': username,
                                                                  'ip': ip['ip'],
                                                                  'email': email})
                db.child("IPS").child(ip_id).update({'used': True})
            except:
                print("ERROR: cant add new user")
    else:
        print("passwords not match!")
        
        
def login(email, password):
    stats = None
    try:
        stats = db.child('Users').order_by_child('email').equal_to(email).get().val()
    except:
        print('ERROR: cant get the stats')
    token = 0
    try:
        token = auth.sign_in_with_email_and_password(email, password)  # Sign up with email and password
        print("User successfully logged in!")
        flag = True
    except:
        flag = False
        print("ERROR: Wrong Email or Password input!")
    if flag is True:
        for name, stat in stats.items():
            return name, stat['ip'], token['idToken']
            

def delete_user(username, token, email):
    sure = input("to verify the delete of the account type the username <" + username + ">: ")
    if sure == username:
        del_user(token, email)
    else:
        print('i guess you not that sure...')

            
def del_user(token, email):
    stats = None
    try:
        stats = db.child('Users').order_by_child('email').equal_to(email).get().val()
    except:
        print('ERROR: cant get the stats')
    try:
        auth.delete_user_account(token)
        flag = True
    except:
        print("cant delete user")
        flag = False
    if flag is True:
        ips = None
        for name, stat in stats.items():
            try:
                db.child('Users').child(name).set(None)
                ips = db.child('IPS').order_by_child('ip').equal_to(stat['ip']).get().val()
            except:
                print('ERROR: cant delete user')
        for ip_id, ip in ips.items():
            try:
                db.child('IPS').child(ip_id).child('used').set('false')
            except:
                print('ERROR: cant change ip to not used')
            return
