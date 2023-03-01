import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
class window:
    email=""
    password=""
    serverIp=""
    command=""
    filepath=""
    combobox=""
    root=tk.Tk()
    mydata=[]
    def __init__(self):
        self.CreateWindow()


    
    def ComboClick(self,event):
        return self.Combobox.get()

    def Upload(self):
        window.mydata.append(window.email.get())
        window.mydata.append(window.password.get())
        window.mydata.append(window.serverIp.get())
        window.mydata.append(window.combobox.get())

        window.root.withdraw()
        file_path = filedialog.askopenfilename()
        window.root.deiconify()
        window.mydata.append(file_path)
        window.root.destroy()
        #print(window.mydata)
    def return_mydata(self):
        return window.mydata



    def getdata(self):

        return window.email.get()
      

    def CreateWindow(self):
        window.root.geometry("500x500")
        window.root.title("File Transferer 2.0")
        icon = tk.PhotoImage(file="resource/icon.png")
        window.root.iconphoto(False, icon)
        panelframe=tk.Frame(window.root)
        panelframe.columnconfigure(0, weight=1)
        panelframe.columnconfigure(1,weight=1)

        label_email=tk.Label(panelframe,text="Email: ",font=("Times New Roman",16))
        label_email.grid(row=0,column=0,padx=10,pady=10,sticky="wn")
        textbox_email=tk.Entry(panelframe,font=("Times New Roman",16))
        textbox_email.grid(row=0, column=1,padx=10,pady=10,sticky="wn")
        window.email=textbox_email


        label_password=tk.Label(panelframe,text="Password: ",font=("Times New Roman",16))
        label_password.grid(row=1,column=0,padx=10,pady=10,sticky="wn")
        textbox_password=tk.Entry(panelframe,font=("Times New Roman",16))
        textbox_password.grid(row=1, column=1,padx=10,pady=10,sticky="wn")
        window.password=textbox_password

        label_server=tk.Label(panelframe,text="Server(IP): ",font=("Times New Roman",16))
        label_server.grid(row=2,column=0,padx=10,pady=10,sticky="wn")
        textbox_IP=tk.Entry(panelframe,font=("Times New Roman",16))
        textbox_IP.grid(row=2, column=1,padx=10,pady=10,sticky="wn")
        window.serverIp=textbox_IP

        label_Command=tk.Label(panelframe,text="Select Command: ",font=("Times New Roman",16))
        label_Command.grid(row=3,column=0,padx=10,pady=10,sticky="wn")
        options=["UPLOAD","DOWNLOAD","LIST","DELETE"]
        Combobox=ttk.Combobox(panelframe,value=options,font=("Times New Roman",16))
        Combobox.current(0)
        Combobox.bind("<<ComboboxSelected>>",self.ComboClick)
        Combobox.grid(row=3,column=1,sticky="wn",padx=10,pady=10)
        window.combobox=Combobox
        btn_upload=tk.Button(panelframe,text="UPLOAD(^)",command=self.Upload,font=("Times New Roman",16))
        btn_upload.grid(row=4,column=0,padx=10,pady=10,columnspan=2)


        panelframe.pack()
        window.root.mainloop()

def main():
    print("About to run Object")
    front=window()

    print("here")
    print(front.return_mydata())



main()