import socket

def get_n_print():
    Response = ClientSocket.recv(512)
    print(Response.decode())
def enter_n_send():
    inp = Input()
    ClientSocket.send(str.encode(inp))
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 10000
print('try to connect..')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

get_n_print()
enter_n_send()
get_n_print()

while True:
    Input = input('Say Something (to disconnect write "quit"): ')
    ClientSocket.send(str.encode(Input))
    if Input.lower() == 'quit':
        break
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()