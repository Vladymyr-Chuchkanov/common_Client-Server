#var 16 SeaBattle
import socket
import numpy as np
import pandas as pd
import random as rnd
import pickle
key_horisontal = ["a","b","c","d","e","f","g","h","i","j"]
key_vertical = [1,2,3,4,5,6,7,8,9,0]
fr = np.full((10,10),0,dtype = int)
field = pd.DataFrame(fr,index = key_vertical,columns=key_horisontal)
fr2= np.full((10,10),0,dtype = int)

i = 0
while i !=2:
    x = rnd.randint(0,9)
    y = rnd.randint(0,9)
    if field.iloc[x,y]==0 and x<8 and field.iloc[x+2,y]==0:
        field.iloc[max(0,x - 1):min(10,x + 4), max(0,y - 1):min(10,y + 2)] = 1
        field.iloc[x:x+3,y]='x'
        i+=1
    if field.iloc[x,y]==0 and y<8 and field.iloc[x,y+2]==0:
        field.iloc[max(0,x - 1):min(10,x + 2), max(0,y - 1):min(10,y + 4)] = 1
        field.iloc[x,y:y+3]='x'
        i+=1
i =0
while i !=3:
    x = rnd.randint(0,9)
    y = rnd.randint(0,9)
    if field.iloc[x,y]==0 and x!=9 and field.iloc[x+1,y]==0:
        field.iloc[max(0,x - 1):min(10,x + 3), max(0,y - 1):min(10,y + 2)] = 1
        field.iloc[x:x+2,y]='y'
        i+=1
    if field.iloc[x,y]==0 and y!=9 and field.iloc[x,y+1]==0:
        field.iloc[max(0,x - 1):min(10,x + 2), max(0,y - 1):min(10,y + 3)] = 1
        field.iloc[x,y:y+2]='y'
        i+=1
i =0
while i !=4:
    x = rnd.randint(0,9)
    y = rnd.randint(0,9)
    if field.iloc[x,y]==0:
        field.iloc[max(0,x - 1):min(10,x + 2), max(0,y - 1):min(10,y + 2)] = 1
        field.iloc[x,y]='z'
        i+=1
#basic field created!
field1 = pd.DataFrame(fr2,index = key_vertical,columns=key_horisontal)
print(field)

s = socket.socket()
print("created!")
port = 11111
s.bind(('', port))
print("bind to %s"%(port))

s.listen(5)
print("listening")
c, addr = s.accept()
ships = 0;
miss = 0;
trueshots = 0;
ll = "ok"
while True:

    print(1)
    data_ = c.recv(4096)

    print(2)
    if not data_:
        break
    g = data_.decode()
    if g== "exit":
        str1 = "ships destroyed:"+str(ships)+"; Shots missed:"+ str(miss)+ "; Shots hit the target:"+ str(trueshots)
        c.send(str1.encode())
        break
    if g== "result":
        ll = "ships destroyed:"+str(ships)+"; Shots missed:"+ str(miss)+ "; Shots hit the target:"+ str(trueshots)

        c.send(ll.encode())
        data = pickle.dumps(field1)
        c.sendall(data)
        continue


    ff = [0,0]
    o = 0
    print (g)
    if len(g)!=2 and g!="result":
        ll = "eri"
        c.send(ll.encode())
        data = pickle.dumps(field1)
        c.sendall(data)
        continue
    b = 77
    for i in g:

        if i == "1" or i=="a":
            b = 0
        elif i == "2" or i=='b':
            b = 1
        elif i == "3" or i=="c":
            b = 2
        elif i == "4" or i=="d":
            b = 3
        elif i == "5" or i=="e":
            b = 4
        elif i == "6" or i=="f":
            b = 5
        elif i == "7" or i=="g":
            b = 6
        elif i == "8" or i=="h":
            b = 7
        elif i == "9" or i=="i":
            b = 8
        elif i == "0" or i=="j":
            b = 9
        else:
            ll = "eri"
            break
        ff[o]=b
        o+=1

    print(ff)
    if field.iloc[ff[1],ff[0]]=="z":
        ships+=1
        trueshots+=1
        field.iloc[max(0, ff[1] - 1):min(10, ff[1] + 2), max(0, ff[0] - 1):min(10, ff[0] + 2)] = "$"
        field1.iloc[max(0, ff[1] - 1):min(10, ff[1] + 2), max(0, ff[0] - 1):min(10, ff[0] + 2)] = "$"
        field1.iloc[ff[1], ff[0]] = "x"
    if field.iloc[ff[1],ff[0]]=="y":
        field.iloc[ff[1], ff[0]] = "d"
        for i in range(max(0,ff[1]-1),min(10,ff[1]+2)):
            for j in range(max(0, ff[0] - 1), min(10, ff[0] + 2)):
                if field.iloc[i,j]=="y":
                    field1.iloc[ff[1], ff[0]] = "x"
                    field.iloc[ff[1], ff[0]] = "d"
                    trueshots += 1
                elif field.iloc[i,j]=="d"and (i !=ff[1]or j!=ff[0]):
                    field.iloc[max(0, ff[1] - 1):min(10, ff[1] + 2), max(0, ff[0] - 1):min(10, ff[0] + 2)] = "$"
                    field.iloc[max(0, i - 1):min(10, i + 2), max(0, j - 1):min(10, j + 2)] = "$"
                    field1.iloc[max(0, ff[1] - 1):min(10, ff[1] + 2), max(0, ff[0] - 1):min(10, ff[0] + 2)] = "$"
                    field1.iloc[max(0, i - 1):min(10, i + 2), max(0, j - 1):min(10, j + 2)] = "$"
                    field1.iloc[i, j] = 'x'
                    field1.iloc[ff[1], ff[0]] = 'x'
                    ships += 1
    check = [0,0,0]
    if field.iloc[ff[1],ff[0]]=="x":
        field.iloc[ff[1], ff[0]] = "d"
        field1.iloc[ff[1], ff[0]] = "x"
        trueshots += 1
        for i in range(max(0, ff[1] - 1), min(10, ff[1] + 2)):
            for j in range(max(0, ff[0] - 1), min(10, ff[0] + 2)):
                if field.iloc[i, j] == "x":
                    field1.iloc[ff[1], ff[0]] = "x"
                    field.iloc[ff[1], ff[0]] = "d"
                elif field.iloc[i,j]=="d"and (i !=ff[1]or j!=ff[0]):
                    check[0]+=1
                    check[1]=i
                    check[2]=j
    print(check)
    if check[0]==1:
        check[0]=0
        ff[1]=check[1]
        ff[0]=check[2]
        field.iloc[ff[1], ff[0]] = "d"
        field1.iloc[ff[1], ff[0]] = "x"
        for i in range(max(0, ff[1] - 1), min(10, ff[1] + 2)):
             for j in range(max(0, ff[0] - 1), min(10, ff[0] + 2)):
                if field.iloc[i, j] == "x":
                    field1.iloc[ff[1], ff[0]] = "x"
                    field.iloc[ff[1], ff[0]] = "d"
                elif field.iloc[i, j] == "d" and (i != ff[1] or j != ff[0]):
                    check[0] += 1
                    check[1] = i
                    check[2] = j
    print(check)
    if(check[0]==2):
        field.iloc[max(0, check[1] - 1):min(10, check[1] + 2), max(0, check[2] - 1):min(10, check[2] + 2)] = "$"
        field.iloc[max(0, ff[1]-(check[1]-ff[0]) - 1):min(10, ff[1]-(check[1]-ff[0]) + 2), max(0, ff[0]-(check[2]-ff[0]) - 1):min(10, ff[0]-(check[2]-ff[0]) + 2)] = "$"
        field1.iloc[max(0, check[1] - 1):min(10, check[1] + 2), max(0, check[2] - 1):min(10, check[2] + 2)] = "$"
        field1.iloc[max(0, ff[1] - (check[1] - ff[1]) - 1):min(10, ff[1] - (check[1] - ff[1]) + 2),max(0, ff[0] - (check[2] - ff[0]) - 1):min(10, ff[0] - (check[2] - ff[0]) + 2)] = "$"
        field1.iloc[ff[1],ff[0]]="x"
        field1.iloc[check[1], check[2]] = "x"
        field1.iloc[ff[1]-(check[1] - ff[1]), ff[0]-(check[2] - ff[0])] = "x"
        ships += 1

    if field.iloc[ff[1],ff[0]]==1 or field.iloc[ff[1],ff[0]]==0:
        field.iloc[ff[1], ff[0]] = '*'
        field1.iloc[ff[1], ff[0]] = '*'
        miss+=1


    if ships == 9:
        ll = "end"
        c.send(ll.encode())
        str = "ships destroyed:" + ships + "; Shots missed:" + miss + "; Shots hit the target:" + trueshots
        c.send(str.encode())
        break

    if g!="result":
        c.send(ll.encode())

    data = pickle.dumps(field1)
    c.sendall(data)

    print(4)


outp = 'bye'
c.send(outp.encode())
c.close()
