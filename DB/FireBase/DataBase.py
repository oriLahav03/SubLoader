import pyrebase

from dotenv import load_dotenv
import os
import ast

load_dotenv()

firebaseConfig = ast.literal_eval(os.getenv('FIREBASE_KEY'))

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

