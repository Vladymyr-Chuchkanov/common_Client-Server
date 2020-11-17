import socket
import pickle
s = socket.socket()
dataArray = bytearray()
port = 11111
s.connect(('127.0.0.1',port))
print("print 'result' to get your current result, print 'exit' to finish your game."
      " You should print yor hit like 'a3' a-j 1-9+0, incorrect input will not influence your game")
while True:
    g = input()
    s.send(g.encode())
    k = s.recv(4096).decode()
    if g == "exit":
        print(k)
        break
    if g == "result":
        print(k)
    if k == "eri":
        print("your input is incorrect")
    data = s.recv(4096)
    df = pickle.loads(data)
    print(df)
print(s.recv(4096).decode())
s.close()



