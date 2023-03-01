import os
import socket



IP=socket.gethostname()
Port=4466
ADDR=(IP,Port)
SIZE=1024
FORMAT="utf-8"
SERVER_DATA_PATH="server_data"

def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data=client.recv(SIZE).decode(FORMAT)
        cmd,msg=data.split("@")
        if(cmd=="OK"):
            print(f"{msg}")
        elif cmd=="DISCONNECTED":
            print(f"{msg}")
            break

        data=input("> ")
        data=data.split(" ")
        cmd=data[0].upper()

        if(cmd=="HELP"):
            client.send(cmd.encode(FORMAT))

        elif cmd=="LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd=="LIST":
            client.send(cmd.encode(FORMAT))
            pass

        elif cmd=="UPLOAD":
            ##Upload@filename@text
            

            path=data[1]
            with open(f"{path}","r") as f:
                text=f.read()
            #clientdata,data.txt
            filename=path.split('/')[-1]
            send_data=f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))

        elif cmd=="DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        
        
    print("Disconnected from the server.")
    client.close()

if(__name__=='__main__'):
    main()


