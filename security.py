from logging import disable
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import BOLD
import mysql.connector
from datetime import datetime

root = Tk()
root.title("Security")
root.config(bg='#1B1F3B')
root.geometry('1920x1080')


def changepassword():
    usr=simpledialog.askstring("Change Credentials", "Enter New Username")
    if usr:
        pass1=simpledialog.askstring("Change Credentials", "Enter New Password", show='*')
        if pass1:
            pass2=simpledialog.askstring("Change Credentials", "Enter New Password Again", show='*')
            if pass2:
                if pass1 == pass2:
                    print(pass1)
                    mydb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
                    cursor = mydb.cursor()
                    sql = "Update Login SET Username = '{}', Password = '{}' WHERE WarehouseName = '{}' && Application = 'SECURITY'".format(usr, pass1, WarehouseName)
                    cursor.execute(sql)
                    mydb.commit()
                    mydb.close()
                    messagebox.showinfo("Change Credentials", "Credentials Changed Succesfully.")
                else:
                    retry = messagebox.askretrycancel("Change Credentials", "Credentials Not Changed \nPlease Enter Password Carefully.")
                    if retry:
                        return changepassword()



def login():
    Application = 'SECURITY'
    global WarehouseName
    WarehouseName = WarehouseLoginDef.get()
    username = username_entry.get()
    password = password_entry.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    sql = "SELECT * FROM Login WHERE WarehouseName = '{}' && Application = '{}' && Username = '{}' && Password = '{}';".format(WarehouseName, Application, username, password)
    mycursor.execute(sql)
    records = mycursor.fetchall()
    if records:
        changepass.config(state=NORMAL)
        operationTab.pack()
        outboundArrData()
        outboundExpData()
        inboundArrData()
        inboundExpData()
        Login.destroy()
        Login.update()

    else:
        login_Res.config(text='Please enter correct details.')

mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
mycursor = mysqldb.cursor()
mycursor.execute("SELECT WarehouseName FROM Warehouse")
records = mycursor.fetchall()
WarehouseList=[r for r, in records]


Login= Toplevel(root)
Login.config(bg='#C9DDFF')
Login.geometry("340x200")
Login.title("Login")

Login.columnconfigure(0, weight=1)
Login.columnconfigure(1, weight=3)
global WarehouseLoginDef
WarehouseLoginDef = StringVar()
WarehouseLoginDef.set(WarehouseList[0])
warehouse_label = Label(Login, text="Warehouse:", bg='#C9DDFF', font=("Arial",15, BOLD))
warehouse_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)

warehouse_OM = OptionMenu(Login, WarehouseLoginDef, *WarehouseList)
warehouse_OM.grid(column=1, row=0, sticky=E, padx=5, pady=5)


username_label = Label(Login, text="Username:", bg='#C9DDFF', font=("Arial",15, BOLD))
username_label.grid(column=0, row=1, sticky=W, padx=5, pady=5)

username_entry = Entry(Login, font=("Arial",12))
username_entry.grid(column=1, row=1, sticky=E, padx=5, pady=5)

password_label = Label(Login, text="Password:", bg='#C9DDFF', font=("Arial",15, BOLD))
password_label.grid(column=0, row=2, sticky=W, padx=5, pady=5)

password_entry = Entry(Login,  show="*", font=("Arial",12))
password_entry.grid(column=1, row=2, sticky=E, padx=5, pady=5)

login_button = Button(Login, text="Login", command=login, font=("Arial",15))
login_button.grid(column=0, row=3, columnspan=2, sticky=NS, padx=5, pady=5)

login_Res = Label(Login, text="", bg='#C9DDFF',fg='RED', font=("Arial",15))
login_Res.grid(column=0, row=4, columnspan=2, sticky=NS, padx=5, pady=5)



operator = "Creative's"

topBar = Frame(root, bg='#1B1F3B', width=1920, height=1080)

title = Label(topBar, text="Security | ", font=("Arial",15, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=0)
name = Label(topBar, text=operator, font=('Arial', 12, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=1)
changepass = Button(topBar, text='Change Login Credentials',command=changepassword, state=DISABLED, font=('Arial', 8))
changepass.grid(row=0, column=2, padx=5)


operationTab= ttk.Notebook(root, width=1920, height=1080)

inboundFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
outboundFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
ansFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)


operationTab.add(inboundFrame, text='Inbound')
operationTab.add(outboundFrame, text='Outbound')
operationTab.add(ansFrame, text='ASN')


inbListTab= ttk.Notebook(inboundFrame, width=1920, height=1080)

inboundArrFrame= Frame(inbListTab, bg='#C9DDFF', width=1920, height=1080)
inboundExpFrame= Frame(inbListTab, bg='#C9DDFF', width=1920, height=1080)

inbListTab.add(inboundExpFrame, text='Expected')
inbListTab.add(inboundArrFrame, text='Arrived')



outbListTab= ttk.Notebook(outboundFrame, width=1920, height=1080)

outboundArrFrame= Frame(outboundFrame, bg='#C9DDFF', width=1920, height=1080)
outboundExpFrame= Frame(outboundFrame, bg='#C9DDFF', width=1920, height=1080)

outbListTab.add(outboundExpFrame, text='Expected')
outbListTab.add(outboundArrFrame, text='Arrived')




topBar.pack()
inbListTab.pack()
outbListTab.pack()

def seeAns(id):
    operationTab.select(2)
    ansSearch.delete(0, END)
    ansSearch.insert(0, id)
    fetchAns()


def outboundArrData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.Status, Stock.Date, Stock.Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status != 'Expected' && ANS.Type = 'Outbound' && ANS.Warehouse = '{}'".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh1=Button(outboundArrFrame, text="Refrsh", command=outboundArrFramerf).grid(row=0,column=0)
    outboundArrCol1=Label(outboundArrFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    outboundArrCol3=Label(outboundArrFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    outboundArrCol5=Label(outboundArrFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    outboundArrCol6=Label(outboundArrFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=5)
    outboundExpCol6=Label(outboundArrFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=6)
    for i, (id, Status, Date, Time) in enumerate(records, start=1):

        outboundArrCol1=Label(outboundArrFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(outboundArrFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol5=Label(outboundArrFrame, text=Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundArrFrame, text=Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundArrFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()


def outboundExpData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.status, ANS.Exp_Date, ANS.Exp_Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.status = 'Expected'  && ANS.Type = 'Outbound' && ANS.Warehouse = '{}' ORDER BY id;".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh2=Button(outboundExpFrame, text="Refrsh", command=outboundExpFramerf).grid(row=0,column=0)
    outboundExpCol1=Label(outboundExpFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    outboundExpCol3=Label(outboundExpFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    outboundExpCol4=Label(outboundExpFrame, text="Acton", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=3)
    outboundExpCol5=Label(outboundExpFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    outboundExpCol5=Label(outboundExpFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=5)
    outboundExpCol6=Label(outboundExpFrame, text="ASN", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=6)
    for i, (id, Status, Exp_Date, Exp_Time) in enumerate(records, start=1):

        outboundArrCol1=Label(outboundExpFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(outboundExpFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Button(outboundExpFrame, text="Allow Entry", command=lambda i = id :outboundEntry(i)).grid(row=i,column=3)
        outboundArrCol5=Label(outboundExpFrame, text=Exp_Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundExpFrame, text=Exp_Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundExpFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()

def inboundArrData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.Status, Stock.Date, Stock.Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status != 'Expected' && ANS.Type = 'Inbound' && ANS.Warehouse = '{}';".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh3=Button(inboundArrFrame, text="Refrsh", command=inboundArrFramerf).grid(row=0,column=0)
    inboundArrCol1=Label(inboundArrFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    inboundArrCol3=Label(inboundArrFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    inboundArrCol5=Label(inboundArrFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    inboundArrCol5=Label(inboundArrFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=5)
    inboundArrCol6=Label(inboundArrFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=6)
    for i, (id,Status, Date, Time) in enumerate(records, start=1):

        outboundArrCol1=Label(inboundArrFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(inboundArrFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol5=Label(inboundArrFrame, text=Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(inboundArrFrame, text=Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(inboundArrFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()
    
def inboundExpData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.status, ANS.Exp_Date, ANS.Exp_Time FROM Stock  JOIN ANS ON Stock.id = ANS.id WHERE Stock.status = 'Expected'  && ANS.Type = 'Inbound' && ANS.Warehouse = '{}' ORDER BY id;".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh4=Button(inboundExpFrame, text="Refrsh", command=inboundExpFramerf).grid(row=0,column=0)
    inboundExpCol2=Label(inboundExpFrame, text="Id", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    inboundExpCol3=Label(inboundExpFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    inboundExpCol4=Label(inboundExpFrame, text="Action", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=3)
    inboundExpCol5=Label(inboundExpFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    inboundExpCol6=Label(inboundExpFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=5)
    inboundExpCol6=Label(inboundExpFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=6)
    for i, (id, Status, Exp_Date, Exp_Time) in enumerate(records, start=1):
        outboundArrCol1=Label(inboundExpFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol2=Label(inboundExpFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol3=Button(inboundExpFrame, text="Allow Entry", command=lambda i = id :inboundEntry(i)).grid(row=i,column=3)
        outboundArrCol4=Label(inboundExpFrame, text=Exp_Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(inboundExpFrame, text=Exp_Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(inboundExpFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()

def outboundArrFramerf():
    for widgets in outboundArrFrame.winfo_children():
        widgets.destroy()
    outboundArrData()

def outboundExpFramerf():
    for widgets in outboundExpFrame.winfo_children():
        widgets.destroy()
    outboundExpData()
def inboundArrFramerf():
    for widgets in inboundArrFrame.winfo_children():
        widgets.destroy()
    inboundArrData()
def inboundExpFramerf():
    for widgets in inboundExpFrame.winfo_children():
        widgets.destroy()
    inboundExpData()

# Main Logic
def inboundEntry(id):
    today = datetime.today()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS")
    cursor = mydb.cursor()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    sql = "UPDATE Stock SET Status = 'Arrived', Date='{}', Time='{}' WHERE id = {}".format(date, time, id)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    inboundArrFramerf()
    inboundExpFramerf()

def outboundEntry(id) :
    today = datetime.today()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS")
    cursor = mydb.cursor()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    sql = "UPDATE Stock SET Status = 'Arrived', Date='{}', Time='{}' WHERE id = {}".format(date, time, id)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    outboundArrFramerf()
    outboundExpFramerf()

def fetchAns():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    cursor = mysqldb.cursor()

    sql = "SELECT * FROM ANS WHERE id ='{}'".format(ansSearch.get())
    cursor.execute(sql)
    records = cursor.fetchall()
    if not cursor.rowcount:
        idData.config(text = '-')
        VehicleTypeData.config(text = '-')
        vehicleNoData.config(text = '-')
        WarehouseData.config(text = '-')
        WarehouseNoData.config(text = '-')
    else:
        for data in records:
            idData.config(text = data[0])
            VehicleTypeData.config(text = data[1])
            vehicleNoData.config(text = data[2])
            WarehouseData.config(text = data[3])
            WarehouseNoData.config(text = data[4])
    mysqldb.close()


ansLabel=Label(ansFrame, text='ASN Id:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(row=0, column=0)
ansSearch=Entry(ansFrame)
sp1=Label(ansFrame, text='  ', bg='#C9DDFF').grid(row=0, column=3)
submit=Button(ansFrame, text='Fetch Details', font=("Arial",10, BOLD), command=fetchAns).grid(row=0, column=4)

sp2=Label(ansFrame, text='  ', bg='#C9DDFF').grid(row=1)
sp3=Label(ansFrame, text='  ', bg='#C9DDFF').grid(row=2)

id=Label(ansFrame, text='ASN Id:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=3, column=0)
VehicleType=Label(ansFrame, text='Vehicle Type:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=4, column=0)
vehicleNo=Label(ansFrame, text='Vehicle No.:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=5, column=0)
Warehouse=Label(ansFrame, text='Warehouse Name:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=6, column=0)
WarehouseNo=Label(ansFrame, text='Warehouse No.:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=7, column=0)

idData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
VehicleTypeData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
vehicleNoData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseNoData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))

ansSearch.grid(sticky = W,row=0, column=1)
idData.grid(sticky = W,row=3, column=1)
VehicleTypeData.grid(sticky = W,row=4, column=1)
vehicleNoData.grid(sticky = W,row=5, column=1)
WarehouseData.grid(sticky = W,row=6, column=1)
WarehouseNoData.grid(sticky = W,row=7, column=1)


root.mainloop()