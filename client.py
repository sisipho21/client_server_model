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
           hasher = hashlib.md5()       #Checking for file correctness
           path = data[1]               #File data Path
           #password = data[2]                #File data password for encrypted portion
           with open(f"{path}", "rb") as f:
               content = f.read()
               hasher.update(content)
           print(hasher.hexdigest())
           file_name=path.split('/')[-1]     #Getting Filename from url
           file_size=os.path.getsize(path)
           print(f"File Size:{file_size}")
           data_obtained = cmd
           data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()}'
           client.sendall(data_obtained.encode())


           with open(f"{path}", "rb") as f:     #Reading file onto uploaded version
               count = 0
               while count<file_size:
                file_data=f.read(file_size)

                client.sendall(file_data)
                count += len(file_data)
           f.close()

        elif cmd=="DOWNLOAD":
            fname = data[1]                 #name of file
            path = data[2]                  #path to save file to
            
            send_data=f"{cmd}@{fname}"      #send name of file to server
            client.send(send_data.encode(FORMAT))

            outputpath=os.path.join(path,fname)         #output path for the file, where it will be saved

            fsize = int(client.recv(SIZE))                   #receive file size

            with open(outputpath, "wb") as f:
                count=0
                while count<fsize:
                    file_data = client.recv(fsize)
                    f.write(file_data)
                    count+=len(file_data)
            f.close()

        elif cmd=="DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        else:
            print("You entered an invalid command. Here is a list of commands below:")
            client.send("HELP".encode(FORMAT))
        
        
    print("Disconnected from the server.")
    client.close()

if(__name__=='__main__'):
    main()


