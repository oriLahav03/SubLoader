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

# DataBase


# Add Data

data = {'age': 40,
        'address': 'New York',
        'employed': True,
        'name': 'John Smith'}  # Add new data

db.push(data)  # Push the data to the server

db.child("People").push(data)  # Save data into kind of dir - can be room !!, we can add more .child() and it will add more dirs.
db.child("people").child("MyOwnID").set(data)  # Make MyOwnID the ID of the data instead of giving it a random ID


# Update Data

db.child("people").child("MyOwnID").update({'AddForYou': 'Ilay'})
db.child("people").child("MyOwnID").update({'AddForYou': 'Ilay'})  # replace the name of the id - MyOnwID to Ori Lahav, if we do this with a new key its will just add it :)


# Get Data

people = db.child('Rooms').get()
for person in people.each():
    print(person.val())
    print(person.key())


# Delete

db.child("People").child("person").child("age").remove()  # delete single key from the db
db.child("People").child("person").remove()  # delete full category

