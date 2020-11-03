import socket
s = socket.socket()
print("created!")
port = 11111
s.bind(('', port))
print("bind to %s"%(port))

s.listen(5)
print("listening")
while True:
    c, addr = s.accept()
    print("got connection from ", addr)
    outp = 'bye'
    c.send(outp.encode())
    c.close()
