import pyrebase

firebaseConfig = {'apiKey': "AIzaSyDBYHK7-ZaFOm1w2gdJB-4BXs3H7M2exZ8",
    'authDomain': "subloadertest.firebaseapp.com",
    'databaseURL': "https://subloadertest.firebaseio.com",
    'projectId': "subloadertest",
    'storageBucket': "subloadertest.appspot.com",
    'messagingSenderId': "1024386391643",
    'appId': "1:1024386391643:web:e2f7df6f0428993971297e",
    'measurementId': "G-DBZRVXNL28"}

firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()
auth = firebase.auth()
# storage = firebase.storage()

print("""
To Login press 1
To Signup press 2
""")
choose = int(input("enter your command: "))

# Authentication

if choose == 1:  # Login
    email = input("enter your Email: ")
    password = input("enter your password: ")
    try:
        auth.sign_in_with_email_and_password(email, password)  # Login with email and password
        print("Successfully signed in!")
    except:
        print("Invalid user or password. Please try again!")

elif choose == 2:  # Signup
    email = input("enter your Email: ")
    password = input("enter your password: ")
    confirmPassword = input("Confirm your password: ")
    if password == confirmPassword:
        try:
            auth.create_user_with_email_and_password(email, password)  # Sign up with email and password
            print("User successfully created!")
        except:
            print("Email already exists!")
    else:
        print("passwords not match!")




























'''
from firebase import firebase

database = firebase.FirebaseApplication("https://subloadertest.firebaseio.com/", None)

data = {
    'Name': 'Ori Lahav',
    'Email': 'oril20503@gmail.com',
    'Phone': '0507205511'
}

result = database.post("/subloadertest/Customer", data)
print(result)
'''