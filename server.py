import os
import socket
import threading
import hashlib

IP=socket.gethostname()
Port=4474
ADDR=(IP,Port)
SIZE=1024
FORMAT="utf-8"
SERVER_DATA_PATH="server_data"
file_text=""

def help_string():
    send_data="OK@"
    send_data+="LIST: List all the files from the server.\n"
    send_data+="UPLOAD <path> <Optional : Private Key>:Upload a file to the server.\n"
    send_data+="DOWNLOAD <filename> <local directory to save file>:Download a file from the server to your specified directory.\n"
    send_data+="DELETE <filename>: Delete a file from the server.\n"
    send_data+="LOGOUT: Disconnect from the server.\n"
    send_data+="HELP:List all the commands."
    return send_data

def handle_client(conn,addr):
    print(f"[New CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server. Enter 'help'.".encode(FORMAT))
    
    while True:
        data=conn.recv(SIZE).decode()
        if(data.split("@")=="UPLOAD"):
            print("Receiving second File")
            file_text=conn.recv(SIZE).decode(FORMAT)
            print("Text of second file")
            print(file_text.decode(FORMAT))
        data=data.split("@")
        cmd=data[0]
        if(cmd=="HELP"):
            help_data = help_string()
            conn.send(help_data.encode(FORMAT))

        elif cmd=="LOGOUT":
            break

        elif cmd=="LIST":
            files=os.listdir(SERVER_DATA_PATH)
            send_data="OK@"
            if(len(files)==0):
                send_data+="The server directory is empty."
            else:
                send_data+="\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd=="UPLOAD":
                
                client_data = data[1].split(",")
                file_name = client_data[0]
                file_size = int(client_data[1])
                hasher_client=client_data[2]
                print(f"File Size:{file_size}")
                filepath = os.path.join(SERVER_DATA_PATH, file_name)
                print("File Name:"+file_name)
                print(f"File Size:{file_size}")

                with open(filepath, "wb") as f:
                    count=0
                    while count<file_size:
                        file_data = conn.recv(file_size)
                        f.write(file_data)
                        count+=len(file_data)
                f.close()

                hasher_server = hashlib.md5()
                with open(f"{filepath}", "rb") as f:
                    content = f.read()
                    hasher_server.update(content)
                f.close()
                if(hasher_client==hasher_server.hexdigest()):
                    print("File was sent successfully without being altered")
                else:
                    print("File was altered when sent")


                send_data="OK@File uploaded."
                conn.send(send_data.encode(FORMAT))

        elif cmd=="DOWNLOAD":
            fname=data[1]
            
            server_path = os.path.join(SERVER_DATA_PATH, fname)     #path where the file is in the server
            print("Server path:"+ server_path)

            fsize = os.path.getsize(server_path)            #size of the requested file from the server
            print("File size:"+ str(fsize))

            conn.send(str(fsize).encode(FORMAT))            #sending file size to the client

            with open(f"{server_path}", "rb") as f:         #reading in file with bytes
                pro = 0
                while pro<fsize:                #check if the file is done reading
                    file_data=f.read(fsize)
                    conn.sendall(file_data)     #keep on sending file data to client until file end
                    pro += len(file_data)
            f.close()

            send_data="OK@File downloaded."
            conn.send(send_data.encode(FORMAT))


        elif cmd=="DELETE":
            files=os.listdir(SERVER_DATA_PATH)
            send_data="OK@"
            filename=data[1]

            if len(files)==0:
                send_data+="The Server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                    send_data+="File deleted."
                else:
                    send_data+="File not found."
            conn.send(send_data.encode(FORMAT))





    print(f'[Disconnected] {addr} Disconnected')

def main():
    print(f"[STARTING] Server is starting.")
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTENING] Server is listening")

    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
if __name__ =="__main__":
    main()



