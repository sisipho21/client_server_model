import os
import socket
import threading
import hashlib
from cryptography.fernet import Fernet

IP=socket.gethostname()
Port=7700
ADDR=(IP,Port)
SIZE=1024
FORMAT="utf-8"
SERVER_DATA_PATH="server_data/public_files"
file_text=""
visible_name=""



def DeleteFile(privatefile):
    SERVER_DATA="server_data/public_files"
    files = os.listdir(SERVER_DATA)
    filename = privatefile

    if len(files) == 0:
        return
    else:
        if filename in files:
            os.system(f"rm {SERVER_DATA}/{filename}")
            print("File deleted.")
            return
        else:

            return
def CheckHiddenFile(user_email,user_password):
    with open('server_data/protected_data/protected.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split(",")
            if(user_data[0]==user_email):
                if(user_data[1]==user_password):
                    return user_data[2]
    return ""
##Generates functions using the username and surname
def generate_key(username, password):
    # Generate a key from the username and password
    key = Fernet.generate_key()
    filepath="server_data/keys/"+username+"_key.key"
    with open(filepath, 'wb') as file:
        file.write(key)
#Loadkeys from their destination to validate the files
def load_key(username):
    # Load the key from the file
    filepath="server_data/keys/"+username+"_key.key"
    with open(filepath, 'rb') as file:
        key = file.read()
    return key
#encrypts the file to a specific destination
def encrypt_file(username, password, filename):
    f_name=filename
    path="server_data/protected_data/"+filename
    filename=path
    # Generate a key from the username and password
    generate_key(username, password)
    key = load_key(username)
    f = Fernet(key)

    # Read the contents of the file
    with open(filename, 'rb') as file:
        file_data = file.read()

    # Encrypt the file contents
    encrypted_data = f.encrypt(file_data)

    # Write the encrypted data to a new file
    path="server_data/protected_data/"
    filename=path+f_name
    encrypted_filename = f"{os.path.splitext(filename)[0]}_encrypted{os.path.splitext(filename)[1]}"
    print(encrypted_filename)
    with open(f"{encrypted_filename}", 'wb') as file:
        file.write(encrypted_data)

    return encrypted_filename

#Decrypts the file from the the path  server_data/protected_data/
def decrypt_file(username, password, encrypted_filename):
    path="server_data/protected_data/"+encrypted_filename
    encrypted_filename=path
    # Load the key from the file
    key = load_key(username)
    f = Fernet(key)

    # Read the encrypted data from the file
    with open(encrypted_filename, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = f.decrypt(encrypted_data)

    # Write the decrypted data to a new file
    raw_name=os.path.splitext(encrypted_filename)[0].split("/")[-1].split("_")[0]
    path="server_data/public_files/"+raw_name
    print(path)
    decrypted_filename = f"{path}_decrypted{os.path.splitext(encrypted_filename)[1]}"

    with open(decrypted_filename, 'wb') as file:
        file.write(decrypted_data)

    return decrypted_filename

#creates the textfile which is used to manage information relating to the encrypted files
def write_to_file(filename, *args, append=False):
    mode = "a" if append else "w"
    path="server_data/protected_data/"+filename
    with open(f"{path}", mode) as f:
        for text in args:
            f.write(text + "\n")


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
            client_mail=data[1].split(",")[0]
            client_password=data[1].split(",")[1]
            PrivateFileName=CheckHiddenFile(client_mail,client_password)
            print("Email Of Client "+client_mail)
            print("Password Of Client "+client_password)
            print("Name Of Private File "+PrivateFileName)
            if(len(PrivateFileName)==0):

                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"
                if (len(files) == 0):
                    send_data += "The server directory is empty."
                else:
                    send_data += "\n".join(f for f in files)
                conn.send(send_data.encode(FORMAT))
            elif len(PrivateFileName)>0:
                print("Inside Decryption")
                file_public=decrypt_file(client_mail,client_password,PrivateFileName)
                file_public=file_public.split("/")[-1]
                print("Name Of decrypted file:"+file_public)
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"
                if (len(files) == 0):
                    send_data += "The server directory is empty."
                else:
                    send_data += "\n".join(f for f in files)
                DeleteFile(file_public)
                conn.send(send_data.encode(FORMAT))



        elif cmd=="UPLOAD":             #if 'upload', the server takes in the file name and size, and uses these to create a new file in the server that writes to all the data
                command_encrypt=f""
                client_data = data[1].split(",")
                if(len(client_data)==6):
                    command_encrypt=client_data[5]

                file_name = client_data[0]
                file_size = int(client_data[1])
                hasher_client=client_data[2]
                user_email=client_data[3]
                user_password=client_data[4]

                if(len(command_encrypt)==0):
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
                
                elif(len(command_encrypt)>=1):
                    if(command_encrypt=="E"):
                        destination="server_data/protected_data/"+file_name
                        with open(destination, "wb") as f:
                            count=0
                            while count<file_size:
                                file_data = conn.recv(file_size)
                                f.write(file_data)
                                count+=len(file_data)
                        f.close()

                        protected_name=encrypt_file(user_email,user_password,file_name)
                        protected_name=protected_name.split("/")[-1]
                        data_write=f"{user_email},{user_password},{protected_name}"
                        write_to_file("protected.txt",data_write,append=True)
                        
                        #Delete the duplicate File
                        file_directory="server_data/protected_data"
                        files=os.listdir(file_directory)
                        send_data="OK@"
                        filename=data[1]

                        if len(files)==0:
                            print("The Server directory is empty")
                        else:
                            if file_name in files:
                                os.system(f"rm {destination}")
                            else:
                                print("File not found.")
                        

                print("File has been Encrypted by Server")

                send_data="OK@File uploaded."
                conn.send(send_data.encode(FORMAT))

        elif cmd=="DOWNLOAD":           #if 'download', the server sends the file size and data to the client so it creates on its side
            data_length=data[1].split(",")
            delete_file=""

            if(len(data_length)==4):
                fname=data_length[0]
                protectedfilename=data_length[0].split("/")[-1].split(".")[0].split("_")[0]
                protectedfileextension=data_length[0].split("/")[-1].split(".")[1]
                protectedfilename=protectedfilename+"_encrypted."+protectedfileextension

                visible_name=decrypt_file(data_length[1],data_length[2],protectedfilename)
                print("File Downloaded")

            else:
                fname=data[1]
            send_data = "OK@"

            files=os.listdir(SERVER_DATA_PATH)
            if len(files)==0:           #if there are no files in server directory
                send_data+="The Server directory is empty"

            elif not fname in files:    #if file is not found
                send_data+="File not found on server"

            else:                       #if file is found in server directory
                server_path = os.path.join(SERVER_DATA_PATH, fname)     #path where the file is in the server
                print("Server path:"+ server_path)

                fsize = os.path.getsize(server_path)            #size of the requested file from the server
                print("File size:"+ str(fsize))

                dld_svr_hash = hashlib.md5()        #hash variable for file in server
                with open(f"{server_path}", "rb") as f:
                    hash_content = f.read()
                    dld_svr_hash.update(hash_content)

                conn.send(f"{str(fsize)}@{dld_svr_hash.hexdigest()}".encode(FORMAT))            #sending file size to the client

                with open(f"{server_path}", "rb") as f:         #reading in file with bytes
                    pro = 0
                    while pro<fsize:                #check if the file is done reading
                        file_data=f.read(fsize)
                        conn.sendall(file_data)     #keep on sending file data to client until file end
                        pro += len(file_data)

                f.close()
                if (len(data_length) == 4):

                    DeleteFile(fname)

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
