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


def catch_exception_get_db(schema, error):
    values = False
    try:
        values = schema
    except:
        print(error)
    return values


def catch_exception_put_db(schema, error):
    try:
        schema
        return True
    except:
        print(error)
        return False


def get_free_ip():
    ips = catch_exception_get_db(db.child('IPS').order_by_child('used').limit_to_first(1).get().val(),
                                 'ERROR: cant get ip...')
    ip = ips.popitem()
    if ip[1]['used'] is False:
        return ip[0], ip[1]['ip']
    else:
        return 'no'


'''def signup(username, email, password, confirm_password):
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
            catch_exception_put_db(
                db.child("Users").child(email.split('@')[0]).set({'username': username, 'ip': ip,
                                                                  'email': email}), 'ERROR: cant add new user')
            catch_exception_put_db(db.child("IPS").child(ip_id).update({'used': True}), 'ERROR: cant change parameter')
    else:
        print("passwords not match!")'''


def login(email, password):
    token = None
    stats = catch_exception_get_db(db.child('Users').order_by_child('email').equal_to(email).get().val(),
                                   'ERROR: cant get the stats')
    try:
        token = auth.sign_in_with_email_and_password(email, password)  # Sign up with email and password
        print("User successfully logged in!")
        flag = True
    except:
        flag = False
        print("ERROR: Wrong Email or Password input!")
    stat = stats.popitem()
    if flag is True:
        return stat[0], stat[1]['ip'], token['idToken']


def delete_user(username, token, email):
    sure = input("to verify the delete of the account type the username <" + username + ">: ")
    if sure == username:
        del_user(token, email)
    else:
        print('i guess you not that sure...')


def del_user(token, email):
    stats = catch_exception_get_db(db.child('Users').order_by_child('email').equal_to(email).get().val(),
                                   'ERROR: cant get the stats')
    try:
        auth.delete_user_account(token)
        flag = True
    except:
        print("cant delete user")
        flag = False

    if flag is True:
        stat = stats.popitem()
        catch_exception_put_db(db.child('Users').child(stat[0]).set(None), 'ERROR: cant delete user')
        ips = catch_exception_get_db(
            db.child('IPS').order_by_child('ip').equal_to(stat[1]['ip']).get().val(),
            'ERROR: cant get ip')
        ip = ips.popitem()
        catch_exception_put_db(db.child('IPS').child(ip[0]).child('used').set(False),
                               'ERROR: cant change ip to not used')
