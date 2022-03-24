import pyrebase

from dotenv import load_dotenv
import os
import ast

load_dotenv()

firebaseConfig = ast.literal_eval(os.getenv('FIREBASE_KEY'))

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# Read

people = db.child("People").order_by_child("employed").equal_to(True).get()
for person in people.each():
    print(person.val())
