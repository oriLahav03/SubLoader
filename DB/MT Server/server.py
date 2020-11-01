import socket
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 10000
ThreadCount = 0
address = []
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection...\n')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server\n'))
    global ThreadCount
    while True:
        try:
            data = connection.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
        except:
            break

        if not data:
            break
        try:
            connection.sendall(str.encode(reply))
        except:
            break
    ThreadCount -= 1
    print("\n", address[0] + ':' + str(address[1]), " disconnected", "\n")
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
