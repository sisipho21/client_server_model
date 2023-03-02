import os
import socket



IP=socket.gethostname()
Port=4476
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
           data_obtained = cmd
           data_obtained += f'@{file_name},{str(file_size)}'
           client.send(data_obtained.encode())
           send_size=0
           output=b''
           with open(f"{path}","rb") as f:
                print("Inside the Open function")
                while send_size<file_size:
                    file_data=f.read(SIZE)
                    print("Read")
                    output+=file_data
                    client.sendall(file_data)
                    send_size+=len(output)
                    
           

           


            ##Upload@filename@text
           """ print("inside upload in the client side")
            path=data[1]
            file_name=data[1].split('/')[-1]
            f = open(file_name, "rb")
            text=f.read()
            file_size=os.path.getsize(path)
            data_obtained=cmd
            data_obtained+=f'@{file_name},{str(file_size)}'
            client.send(data_obtained.encode())
            client.sendall(text)
        
            print("File has been sent")

            //different code

        
            path=data[1]
            with open(f"{path}","r") as f:
                text=f.read()
            #clientdata,data.txt
            filename=path.split('/')[-1]
            send_data=f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
            """
        elif cmd=="DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
        
        
    print("Disconnected from the server.")
    client.close()

if(__name__=='__main__'):
    main()


