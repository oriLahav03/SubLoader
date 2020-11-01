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

db = firebase.database()

# Read

people = db.child("People").order_by_child("employed").equal_to(True).get()
for person in people.each():
    print(person.val())
