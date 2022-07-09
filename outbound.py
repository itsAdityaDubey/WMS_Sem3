from logging import disable
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import BOLD
import mysql.connector
from datetime import datetime

root = Tk()
root.title("Outbound")
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
    Application = 'OUTBOUND'
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
        outboundUnlData()
        outboundInbData()
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

title = Label(topBar, text="Outbound | ", font=("Arial",15, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=0)
name = Label(topBar, text=operator, font=('Arial', 12, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=1)
changepass = Button(topBar, text='Change Login Credentials',command=changepassword, state=DISABLED, font=('Arial', 8))
changepass.grid(row=0, column=2, padx=5)

operationTab= ttk.Notebook(root, width=1920, height=1080)

ansFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
outboundArrFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
outboundExpFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
outboundUnlFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
outboundInbFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)

operationTab.add(outboundExpFrame, text='Expected')
operationTab.add(outboundArrFrame, text='Arrived')
operationTab.add(outboundUnlFrame, text='Load')
operationTab.add(outboundInbFrame, text='Outbound')
operationTab.add(ansFrame, text='ASN')

topBar.pack()


# Main Logic
def outboundLoad(id):
    today = datetime.today()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS")
    global ArrLogData
    cursor = mydb.cursor()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    sql = "SELECT Stock.id FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status='Loading' && ANS.Warehouse_No = (SELECT Warehouse_No FROM ANS WHERE id = {})".format(id)
    cursor.execute(sql)
    records = cursor.fetchall()
    if not cursor.rowcount:
        sql = "UPDATE Stock SET Status = 'Loading', Unl_Date='{}', Unl_Time='{}' WHERE id = {}".format(date, time, id)
        cursor.execute(sql)
        mydb.commit()
        mydb.close()
        outboundArrFramerf()
        outboundUnlFramerf()
    else:
        for data in records:
            ArrLogData = 'Already Loading ANS Id: {}'.format(data[0])
        outboundArrFramerf()

def outbound(id):
    today = datetime.today()
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS")
    global UnlLogData
    cursor = mydb.cursor()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    sql = "UPDATE Stock SET Status = 'Outbound', Inb_Date='{}', Inb_Time='{}' WHERE id = {}".format(date, time, id)
    UnlLogData = 'ANS Id: {} Outbound'.format(id)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    outboundUnlFramerf()
    outboundInbFramerf()

def seeAns(id):
    operationTab.select(4)
    ansSearch.delete(0, END)
    ansSearch.insert(0, id)
    fetchAns()

ArrLogData = '-'  
UnlLogData = '-'  

def outboundArrData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.Status, Stock.Date, Stock.Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status = 'Arrived' && ANS.Type = 'Outbound' && ANS.Warehouse = '{}';".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh3=Button(outboundArrFrame, text="Refresh", command=outboundArrFramerf).grid(row=0,column=0)
    arrLog=Label(outboundArrFrame, text="Last Action | ", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0, column=1, columnspan=2)
    arrLogData=Label(outboundArrFrame, text=ArrLogData, bg='#C9DDFF', font=("Arial",15))
    arrLogData.grid(sticky = W, row=0, column=3, columnspan=4)
    outboundArrCol1=Label(outboundArrFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=1)
    outboundArrCol3=Label(outboundArrFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=2)
    outboundArrCol4=Label(outboundArrFrame, text="Action", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=3)
    outboundArrCol5=Label(outboundArrFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=4)
    outboundArrCol5=Label(outboundArrFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=5)
    outboundArrCol6=Label(outboundArrFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=6)
    for i, (id,Status, Date, Time) in enumerate(records, start=2):

        outboundArrCol1=Label(outboundArrFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(outboundArrFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Button(outboundArrFrame, text="Load", command=lambda i = id :outboundLoad(i)).grid(row=i,column=3)
        outboundArrCol5=Label(outboundArrFrame, text=Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundArrFrame, text=Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundArrFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()
    
def outboundExpData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.status, ANS.Exp_Date, ANS.Exp_Time FROM Stock  JOIN ANS ON Stock.id = ANS.id WHERE Stock.status = 'Expected'  && ANS.Type = 'Outbound' && ANS.Warehouse = '{}' ORDER BY id;".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh4=Button(outboundExpFrame, text="Refresh", command=outboundExpFramerf).grid(row=0,column=0)
    outboundExpCol2=Label(outboundExpFrame, text="Id", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=1)
    outboundExpCol3=Label(outboundExpFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=2)
    outboundExpCol5=Label(outboundExpFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=4)
    outboundExpCol6=Label(outboundExpFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=5)
    outboundExpCol6=Label(outboundExpFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=6)
    for i, (id, Status, Exp_Date, Exp_Time) in enumerate(records, start=2):
        outboundArrCol1=Label(outboundExpFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol2=Label(outboundExpFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Label(outboundExpFrame, text=Exp_Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundExpFrame, text=Exp_Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundExpFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()

def outboundUnlData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.Status, Stock.Unl_Date, Stock.Unl_Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status = 'Loading' && ANS.Type = 'Outbound' && ANS.Warehouse = '{}';".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh3=Button(outboundUnlFrame, text="Refresh", command=outboundUnlFramerf).grid(row=0,column=0)
    unlLog=Label(outboundUnlFrame, text="Last Action | ", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0, column=1, columnspan=2)
    unlLogData=Label(outboundUnlFrame, text=UnlLogData, bg='#C9DDFF', font=("Arial",15))
    unlLogData.grid(sticky = W, row=0, column=3, columnspan=4)
    outboundArrCol1=Label(outboundUnlFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=1)
    outboundArrCol3=Label(outboundUnlFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=2)
    outboundArrCol4=Label(outboundUnlFrame, text="Action", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=3)
    outboundArrCol5=Label(outboundUnlFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=4)
    outboundArrCol5=Label(outboundUnlFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=5)
    outboundArrCol6=Label(outboundUnlFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=6)
    for i, (id,Status, Unl_Date, Unl_Time) in enumerate(records, start=2):

        outboundArrCol1=Label(outboundUnlFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(outboundUnlFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Button(outboundUnlFrame, text="Load Complete", command=lambda i = id :outbound(i)).grid(row=i,column=3)
        outboundArrCol5=Label(outboundUnlFrame, text=Unl_Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundUnlFrame, text=Unl_Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundUnlFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()

def outboundInbData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Stock.id, Stock.Status, Stock.Inb_Date, Stock.Inb_Time FROM Stock JOIN ANS ON Stock.id = ANS.id WHERE Stock.Status = 'Outbound' && ANS.Type = 'Outbound' && ANS.Warehouse = '{}';".format(WarehouseName))
    records = mycursor.fetchall()

    Refresh3=Button(outboundInbFrame, text="Refresh", command=outboundInbFramerf).grid(row=0,column=0)
    outboundArrCol1=Label(outboundInbFrame, text="ID", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=1)
    outboundArrCol3=Label(outboundInbFrame, text="Status", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=2)
    outboundArrCol5=Label(outboundInbFrame, text="Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=4)
    outboundArrCol5=Label(outboundInbFrame, text="Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=5)
    outboundArrCol6=Label(outboundInbFrame, text="ANS", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=1,column=6)
    for i, (id,Status, Inb_Date, Inb_Time) in enumerate(records, start=2):

        outboundArrCol1=Label(outboundInbFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol3=Label(outboundInbFrame, text=Status, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol5=Label(outboundInbFrame, text=Inb_Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol5=Label(outboundInbFrame, text=Inb_Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(outboundInbFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=6)
        mysqldb.close()
    

def outboundArrFramerf():
    for widgets in outboundArrFrame.winfo_children():
        widgets.destroy()
    outboundArrData()
def outboundExpFramerf():
    for widgets in outboundExpFrame.winfo_children():
        widgets.destroy()
    outboundExpData()
def outboundUnlFramerf():
    for widgets in outboundUnlFrame.winfo_children():
        widgets.destroy()
    outboundUnlData()
def outboundInbFramerf():
    for widgets in outboundInbFrame.winfo_children():
        widgets.destroy()
    outboundInbData()

def fetchAns():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    cursor = mysqldb.cursor()

    sql = "SELECT * FROM ANS WHERE id ='{}' && Type='Outbound'".format(ansSearch.get())
    cursor.execute(sql)
    records = cursor.fetchall()
    if not cursor.rowcount:
        idData.config(text = '-')
        VehicleTypeData.config(text = '-')
        vehicleNoData.config(text = '-')
        WarehouseData.config(text = '-')
        WarehouseNoData.config(text = '-')
        ShippingData.config(text = '-')
    else:
        for data in records:
            idData.config(text = data[0])
            VehicleTypeData.config(text = data[1])
            vehicleNoData.config(text = data[2])
            WarehouseData.config(text = data[3])
            WarehouseNoData.config(text = data[4])
            ShippingData.config(text = data[9])
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
Shipping=Label(ansFrame, text='Shipping:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=8, column=0)

idData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
VehicleTypeData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
vehicleNoData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseNoData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))
ShippingData=Label(ansFrame, text='-', bg='#C9DDFF', font=("Arial",12))

ansSearch.grid(sticky = W,row=0, column=1)
idData.grid(sticky = W,row=3, column=1)
VehicleTypeData.grid(sticky = W,row=4, column=1)
vehicleNoData.grid(sticky = W,row=5, column=1)
WarehouseData.grid(sticky = W,row=6, column=1)
WarehouseNoData.grid(sticky = W,row=7, column=1)
ShippingData.grid(sticky = W,row=8, column=1)


root.mainloop()