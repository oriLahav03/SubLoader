import pyrebase

from dotenv import load_dotenv
import os
import ast

load_dotenv()

firebaseConfig = ast.literal_eval(os.getenv('FIREBASE_KEY'))

firebase = pyrebase.initialize_app(firebaseConfig)

# db = firebase.database()
storage = firebase.storage()

# Storage

print("""
To upload file press 1
To get file URL press 2
To download file press 3
""")

choose = int(input("enter command: "))

if choose == 1:  # Upload files / pics / audio
    fileName = input("Enter the name of the file you want to upload: ")
    cloudFileName = input("Enter the name of the file on the cloud: ")  # we can do files/file.txt and its will put file.txt in a dir called files

    storage.child(cloudFileName).put(fileName)  # put fileName on the cloud with the name cloudFileName

elif choose == 2:  # Get files / pics / audio URL from the cloud
    cloudFileName = input("Enter the name of the file on the cloud: ")
    print(storage.child(cloudFileName).get_url(None))  # give the URL of the file from the cloud

elif choose == 3:  # Download files / pics / audio from the cloud
    cloudFileNameToDownload = input("name of file you wanna download: ")
    # downloadFileName = input("enter the name you wanna save the file as: ")
    # address = input("enter the address of the file: ")
    # if '\'' in address:
        # address.replace('\'', '\\')
    # print(address)
    storage.child(cloudFileNameToDownload).download(r"D:\Downloads", "downloadFileName.txt")  # Download cloudFileNameToDownload from storage
