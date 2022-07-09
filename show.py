import tkinter as tk
from tkinter import ttk
import mysql.connector
 
def show():
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT * FROM customers")
        records = mycursor.fetchall()
        # print(records)

        for i, (name,address) in enumerate(records, start=1):
            listBox.insert("", "end", values=(name, address))
            mysqldb.close()
 
 
root = tk.Tk()
root.title("Records")
label = tk.Label(root, text="Records", font=("Arial",30)).grid(row=0, columnspan=3)
 
cols = ('Name', 'Address')
listBox = ttk.Treeview(root, columns=cols, show='headings')
 
for col in cols:
    listBox.heading(col, text=col)    
    listBox.grid(row=1, column=0, columnspan=2)
closeButton = tk.Button(root, text="Close", width=15, command=exit).grid(row=2, column=0)
closeButton = tk.Button(root, text="Refresh", width=15).grid(row=2, column=1)
show()
root.mainloop()