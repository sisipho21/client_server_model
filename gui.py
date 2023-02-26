import tkinter as tk


root=tk.Tk()
root.geometry("800x500")
root.title("File Transferer 2.0")
label=tk.Label(root,text="Hello World!",font=("Times New Roman",18))
label.pack(padx=20,pady=20)

textbox=tk.Text(root,height=2,font=('Arial',16), width= 20)
textbox.pack()
root.mainloop()