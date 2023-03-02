import os
import socket
import hashlib



IP=socket.gethostname()
Port=4474
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
           hasher = hashlib.md5()
           path = data[1]
           with open(f"{path}", "rb") as f:
               content = f.read()
               hasher.update(content)
           print(hasher.hexdigest())
           file_name=data[1].split('/')[-1]
           file_size=os.path.getsize(path)
           print(f"File Size:{file_size}")
           data_obtained = cmd
           data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()}'
           client.sendall(data_obtained.encode())


           with open(f"{path}", "rb") as f:
               count = 0
               while count<file_size:
                file_data=f.read(file_size)

                client.sendall(file_data)
                count += len(file_data)
           f.close()

        elif cmd=="DOWNLOAD":
            ##Download filename directory 
            fname = data[1]
            path = data[2]
            
            outputpath=os.path.join(path,fname)         #output path for the ne file

            #with open(f"{filepath}","r") as f:
            #    text=f.read()
            #clientdata,data.txt
            #filename=path.split('/')[-1]
            send_data=f"{cmd}@{fname}@{path}@{text}"
            client.send(send_data.encode(FORMAT))

        elif cmd=="DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        
        
    print("Disconnected from the server.")
    client.close()

if(__name__=='__main__'):
    main()


