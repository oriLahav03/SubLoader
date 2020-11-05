import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 10000

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
print(Response.decode())
while True:
    Input = input('Say Something (to disconnect write "quit"): ')
    ClientSocket.send(str.encode(Input))
    if Input.lower() == 'quit':
        break
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()