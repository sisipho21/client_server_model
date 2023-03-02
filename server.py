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

#function returning the help string with commands for user to enter
def help_string():                      
    send_data="OK@"
    send_data+="LIST: List all the files from the server.\n"
    send_data+="UPLOAD <path> <Optional : Private Key>:Upload a file to the server.\n"
    send_data+="DOWNLOAD <filename> <local directory to save file>:Download a file from the server to your specified directory.\n"
    send_data+="DELETE <filename>: Delete a file from the server.\n"
    send_data+="LOGOUT: Disconnect from the server.\n"
    send_data+="HELP:List all the commands."
    return send_data

#function used by the server to handle commands and messages from the client
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

        data=data.split("@")            #splitting message/data from the client with '@' delimeter to obtain the command and other important information
        cmd=data[0]

        if(cmd=="HELP"):                #if command is 'help', send text from help_string function for client to print
            help_data = help_string()
            conn.send(help_data.encode(FORMAT))

        elif cmd=="LOGOUT":             #if cmd is 'logout', exit while loop to disconnect with the client
            break

        elif cmd=="LIST":               #if cmd is 'list', server checks if it has files, and sends them to the client to display them
            files=os.listdir(SERVER_DATA_PATH)
            send_data="OK@"
            if(len(files)==0):
                send_data+="The server directory is empty."
            else:
                send_data+="\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd=="UPLOAD":             #if 'upload', the server takes in the file name and size, and uses these to create a new file in the server that writes to all the data
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

        elif cmd=="DOWNLOAD":           #if 'download', the server sends the file size and data to the client so it creates on its side
            fname=data[1]
            
            send_data = "OK@"

            files=os.listdir(SERVER_DATA_PATH)
            if len(files)==0:
                send_data+="The Server directory is empty"

            elif not fname in files:
                send_data+="File not found on server"

            else:
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

                send_data +="File downloaded."
                
            conn.send(send_data.encode(FORMAT))


        elif cmd=="DELETE":                     #if 'delete', server checks if the file exists and deletes it from the server
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

    print(f'[Disconnected] {addr} Disconnected')        #feedback when connection is terminated with the client

def main():
    #server creates its socket and listens for connections from clients
    print(f"[STARTING] Server is starting.")
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()             
    print("[LISTENING] Server is listening")

    #running infinitely, the server accepts connections from clients, and uses a thread to create a socket for each client, where they communicate
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))      #the thread uses the handle_client method for communication with the client
        thread.start()

if __name__ =="__main__":
    main()



