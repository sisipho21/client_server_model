import os
import socket



IP=socket.gethostname()
Port=4473
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
           
           path=data[1]
           file_name=data[1].split('/')[-1]
           file_size=os.path.getsize(path)
           print(f"File Size:{file_size}")
           data_obtained = cmd
           data_obtained += f'@{file_name},{str(file_size)}'
           client.sendall(data_obtained.encode())
           with open(f"{path}", "rb") as f:
               pro = 0
               while pro<file_size:
                file_data=f.read(file_size)
                client.sendall(file_data)
                pro += len(file_data)
           f.close()
        elif cmd=="DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        
        
    print("Disconnected from the server.")
    client.close()

if(__name__=='__main__'):
    main()


