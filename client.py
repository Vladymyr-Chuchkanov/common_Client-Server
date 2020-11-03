import socket
s = socket.socket()
port = 11111
s.connect(('127.0.0.1',port))
print(s.recv((16)))
s.close()
