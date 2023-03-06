import os
import socket
import hashlib

IP=socket.gethostname()
Port=4458
ADDR=(IP,Port)
SIZE=1024
FORMAT="utf-8"
SERVER_DATA_PATH="server_data"

def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)            #connect with server

    while True:
        data=client.recv(SIZE).decode(FORMAT)
        cmd,msg=data.split("@")     
        if(cmd=="OK"):              #if msg from server starts with 'OK', the client can continue operating, displaying the msg for the user
            print(f"{msg}")
        elif cmd=="DISCONNECTED":   #if msg from server is 'disconnected', the client displays feedback for user and stops running
            print(f"{msg}")
            break


        data=input("> ")            #receive input from the user
        data=data.split(" ")        #splitting the user input to get the user's command in cmd
        cmd=data[0].upper()

        if(cmd=="HELP"):            #if command is help, tell the server to print out the help string
            client.send(cmd.encode(FORMAT))

        elif cmd=="LOGOUT":         #if command is logout, inform server
            client.send(cmd.encode(FORMAT))
            break

        elif cmd=="LIST":           #if cmd is list, let server list its available files
            client.send(cmd.encode(FORMAT))
            pass

        elif cmd=="UPLOAD":         #if cmd is upload, we must obtain the user's path to the file and send it to the server
           user_email=input("Enter Email: ")
           user_password=input("Enter Password: ")
           path = data[1]
           file_name = path.split('/')[-1]
           file_size = os.path.getsize(path)
           hasher = hashlib.md5()
           with open(f"{path}", "rb") as f:
               content = f.read()
               hasher.update(content)

           data_obtained = cmd
           if(len(data)==3):
               data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()},'
               data_obtained += f'{user_email},{user_password},{data[2]}'
           else:
                data_obtained += f'@{file_name},{str(file_size)},{hasher.hexdigest()},'
                data_obtained += f'{user_email},{user_password}'

           print(f"File Size:{file_size}")
           client.sendall(data_obtained.encode())

           with open(f"{path}", "rb") as f:
               count = 0
               while count<file_size:
                file_data=f.read(file_size)

                client.sendall(file_data)
                count += len(file_data)
           f.close()
            

        #if cmd is download, the name of file to be downloaded must be captured, with the directory it must be saved to
        elif cmd=="DOWNLOAD":               
            fname = data[1]                 #name of file
            path = data[2]                  #directory to save file to
            
            send_data=f"{cmd}@{fname}"      #send name of file to server
            client.send(send_data.encode(FORMAT))

            outputpath=os.path.join(path,fname)         #output path for the file, where it will be saved

            server_info = client.recv(SIZE).decode()
            fsize, server_hash = server_info.split('@')

            fsize = int(fsize)              #receive file size from the server

            with open(outputpath, "wb") as f:           #write the file data into the path of user, getting the data from server until the whole file size has been received 
                count=0
                while count<fsize:
                    file_data = client.recv(fsize)
                    f.write(file_data)
                    count+=len(file_data)

            dld_clnt_hash = hashlib.md5()        #hash variable for file in client directory
            with open(f"{outputpath}", "rb") as f:
                hash_content = f.read()
                dld_clnt_hash.update(hash_content)

            #compare server hash and client hash to see if they are the same
            if dld_clnt_hash == server_hash:
                print("File downloaded without alterations")
            else:
                print("File altered during downloading process")

            f.close()                       #close f when done wrting to the file

        elif cmd=="DELETE":                 #if cmd is delete, capture name of file to be deleted, and send it to server
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        else:                               #if the command is not recognised, an error message is displayed, and server is prompted to send the help string for user
            print("You entered an invalid command. Here is a list of commands below:")
            client.send("HELP".encode(FORMAT))
        
        
    print("Disconnected from the server.")  #display feedback message to the user
    client.close()                          #closing the connection when done 

if(__name__=='__main__'):
    main()


