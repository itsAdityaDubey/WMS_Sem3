from logging import disable
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import BOLD
from typing import Collection
import mysql.connector
from datetime import datetime


root = Tk()
root.title("ASN")
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
                    sql = "Update Login SET Username = '{}', Password = '{}' WHERE id = 1".format(usr, pass1)
                    cursor.execute(sql)
                    mydb.commit()
                    mydb.close()
                    messagebox.showinfo("Change Credentials", "Credentials Changed Succesfully.")
                else:
                    retry = messagebox.askretrycancel("Change Credentials", "Credentials Not Changed \nPlease Enter Password Carefully.")
                    if retry:
                        return changepassword()



def login():
    Application = 'ADMIN'
    global WarehouseName
    username = username_entry.get()
    password = password_entry.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    sql = "SELECT * FROM Login WHERE WarehouseName = 'ALL' && Application = '{}' && Username = '{}' && Password = '{}';".format(Application, username, password)
    mycursor.execute(sql)
    records = mycursor.fetchall()
    if records:
        changepass.config(state=NORMAL)
        operationTab.pack()
        ansListData()
        warehouseListData()
        Login.destroy()
        Login.update()
    else:
        login_Res.config(text='Please enter correct details.')
def warehouseListCreate():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT WarehouseName FROM Warehouse")
    records = mycursor.fetchall()
    global WarehouseList
    WarehouseList=[r for r, in records]

warehouseListCreate()

Login= Toplevel(root)
Login.config(bg='#C9DDFF')
Login.geometry("340x200")
Login.title("Login")

Login.columnconfigure(0, weight=1)
Login.columnconfigure(1, weight=3)

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


def createfinalANS(Vehicle_Type, vehicle_No, Warehouse, Warehouse_No, Exp_Date, Exp_Time, Shipping, Type, Cr_Date, Cr_Time):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS"
    )

    cursor = mydb.cursor()

    sql = "INSERT INTO ANS (Vehicle_Type, vehicle_No, Warehouse, Warehouse_No, Exp_Date, Exp_Time, Shipping, Type, Cr_Date, Cr_Time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (Vehicle_Type, vehicle_No, Warehouse, Warehouse_No, Exp_Date, Exp_Time, Shipping, Type, Cr_Date, Cr_Time)
    cursor.execute(sql, val)
    mydb.commit()

    id = cursor.lastrowid

    sql = "INSERT INTO Stock (id, Status, Type) VALUES (%s, %s, %s)"
    val = (id, 'Expected', Type)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return id

def createWharehouse():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT WarehouseName FROM Warehouse")
    records = mycursor.fetchall()
    check=0
    for i, (WarehouseName) in enumerate(records, start=1) :
        if whDef.get() == WarehouseName[0]:
            check = 1
    mysqldb.close()
    today = datetime.today()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")

    
    if check == 0:
        mydb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
        cursor = mydb.cursor()
        sql = "INSERT INTO Warehouse (WarehouseName, Warehouse_No, Date, Time) VALUES ('{}', {} , '{}', '{}')".format(whDef.get(), Wh_NoDef.get(), date, time)
        cursor.execute(sql)
        mydb.commit()
        mydb.close()
        application=['ADMIN', 'SECURITY', 'INBOUND', 'OUTBOUND']
        for apps in application:
            mydb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
            cursor = mydb.cursor()
            sql = "INSERT INTO Login (WarehouseName, Application, Username, Password) VALUES ('{}', '{}' , 'admin', 'admin')".format(whDef.get(), apps)
            cursor.execute(sql)
            mydb.commit()
            mydb.close()
        WhRes.config(text="Warehouse Name : {}, is Created.".format(whDef.get()))
        warehouseListFramerf()
        createwarehousesrf()
    else:
        WhRes.config(text="Warehouse alredy exists. \nPlease make changes to the name.".format(whDef.get()))

def createAns():
    today = datetime.today()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    Res = createfinalANS(vehicletypdef.get(), Vehicle_NoDef.get(), Warehousedef.get(), Warehouse_Nodef.get(), Exp_DateDef.get(), Exp_TimeDef.get(), ShippingDef.get("1.0","end"), typedef.get(), date, time)
    Responce.config(text='ASN Created with ID: {}'.format(Res))
    createwarehousesrf()


operator = "Creative's"

topBar = Frame(root, bg='#1B1F3B', width=1920, height=1080)

title = Label(topBar, text="Admin | ", font=("Arial",15, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=0)
name = Label(topBar, text=operator, font=('Arial', 12, BOLD), bg='#1B1F3B', fg='white').grid(row=0, column=1)
changepass = Button(topBar, text='Change Login Credentials',command=changepassword, state=DISABLED, font=('Arial', 8))
changepass.grid(row=0, column=2, padx=5)


operationTab= ttk.Notebook(root, width=1920, height=1080)

ansFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
ansListFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
ansSearchFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
WarehouseFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)
WarehouseListFrame= Frame(operationTab, bg='#C9DDFF', width=1920, height=1080)

operationTab.add(ansFrame, text='ASN')
operationTab.add(ansListFrame, text='ASN List')
operationTab.add(ansSearchFrame, text='ASN Search')
operationTab.add(WarehouseFrame, text='Create Warehouse')
operationTab.add(WarehouseListFrame, text='Warehouse List')
topBar.pack()

def seeAns(id):
    operationTab.select(2)
    ansSearch.delete(0, END)
    ansSearch.insert(0, id)
    fetchAns()

def fetchwh(id):
    operationTab.select(3)
    global UpdateId 
    UpdateId = id
    WhUpdate.config(state=NORMAL)
    WhSubmit.config(state=DISABLED)
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    cursor = mysqldb.cursor()

    sql = "SELECT * FROM Warehouse WHERE id ='{}'".format(id)
    cursor.execute(sql)
    records = cursor.fetchall()
    for data in records:
        whDef.delete(0, END)
        whDef.insert(0, data[1])
        Wh_NoDef.delete(0, END)
        Wh_NoDef.insert(0, data[2])

    createwarehousesrf()
        

def Updatewh():
    today = datetime.today()
    date = today.strftime("%d/%m/%Y")
    time = today.strftime("%H:%M")
    mydb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    cursor = mydb.cursor()
    sql = "Update Warehouse SET WarehouseName = '{}', Warehouse_No = '{}', Date = '{}', Time = '{}' WHERE id = {} ".format(whDef.get(), Wh_NoDef.get(), date, time, UpdateId)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    WhRes.config(text="Warehouse Id: {} Updated".format(UpdateId))
    WhUpdate.config(state=DISABLED)
    WhSubmit.config(state=NORMAL)
    warehouseListFramerf()
    createwarehousesrf()

def closewh(id):
    mydb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    cursor = mydb.cursor()
    sql = "DELETE FROM Warehouse WHERE id = {} ".format(id)
    cursor.execute(sql)
    mydb.commit()
    mydb.close()
    warehouseListFramerf()
    createwarehousesrf()

def ansListData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id, Vehicle_Type, vehicle_No FROM ANS")
    records = mycursor.fetchall()

    Refresh4=Button(ansListFrame, text="Refrsh", command=ansListFramerf).grid(row=0,column=0)
    inboundExpCol2=Label(ansListFrame, text="Id", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    inboundExpCol3=Label(ansListFrame, text="Vehicle Type", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    inboundExpCol4=Label(ansListFrame, text="Vehicle No", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=3)
    inboundExpCol5=Label(ansListFrame, text="Action", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    for i, (id, Vehicle_Type, vehicle_No) in enumerate(records, start=1):
        outboundArrCol1=Label(ansListFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol2=Label(ansListFrame, text=Vehicle_Type, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Label(ansListFrame, text=vehicle_No, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=3)
        outboundArrCol6=Button(ansListFrame, text="See ASN", command=lambda i = id :seeAns(i)).grid(row=i,column=4)
        mysqldb.close()

def ansListFramerf():
    for widgets in ansListFrame.winfo_children():
        widgets.destroy()
    ansListData()

def warehouseListData() :
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT * FROM Warehouse")
    records = mycursor.fetchall()

    Refresh4=Button(WarehouseListFrame, text="Refrsh", command=warehouseListFramerf).grid(row=0,column=0)
    inboundExpCol2=Label(WarehouseListFrame, text="Id", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=1)
    inboundExpCol3=Label(WarehouseListFrame, text="WarehouseName", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=2)
    inboundExpCol4=Label(WarehouseListFrame, text="Warehouse No", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=3)
    inboundExpCol4=Label(WarehouseListFrame, text="Establisment Date", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=4)
    inboundExpCol4=Label(WarehouseListFrame, text="Establisment Time", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=5)
    inboundExpCol5=Label(WarehouseListFrame, text="Action", bg='#C9DDFF', font=("Arial",15, BOLD)).grid(row=0,column=6)
    for i, (id, WarehouseName, Warehouse_No, Date, Time) in enumerate(records, start=1):
        outboundArrCol1=Label(WarehouseListFrame, text=id, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=1)
        outboundArrCol2=Label(WarehouseListFrame, text=WarehouseName, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=2)
        outboundArrCol4=Label(WarehouseListFrame, text=Warehouse_No, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=3)
        outboundArrCol4=Label(WarehouseListFrame, text=Date, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=4)
        outboundArrCol4=Label(WarehouseListFrame, text=Time, bg='#C9DDFF', font=("Arial",15)).grid(row=i,column=5)
        outboundArrCol6=Button(WarehouseListFrame, text="Update", command=lambda i = id :fetchwh(i)).grid(row=i,column=6)
        outboundArrCol7=Button(WarehouseListFrame, text="Close Permanentely", command=lambda i = id :closewh(i)).grid(row=i,column=7)
        mysqldb.close()

def warehouseListFramerf():
    for widgets in WarehouseListFrame.winfo_children():
        widgets.destroy()
    warehouseListData()


def warehousehNolist(id):
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT Warehouse_No FROM Warehouse WHERE id={}".format(id))
    records = mycursor.fetchall()
    global WarehouseNoList
    WarehouseNoList=[]
    for data in records :
        NoWarehouse = data[0]
        for x in range(1, NoWarehouse+1) :
            WarehouseNoList.append(x)
   
def changewh(*args):
    whName=Warehousedef.get()
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="my_password", database="testWMS")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id FROM Warehouse WHERE WarehouseName='{}'".format(whName))
    records = mycursor.fetchall()
    for data in records :
        id = data[0]
        warehousehNolist(id)
        Warehouse_NoDef.destroy()
        createwhno()
        Warehouse_Nodef.set(WarehouseNoList[0])


Wh=Label(WarehouseFrame, text='Warehouse:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=1, column=0)
Wh_No=Label(WarehouseFrame, text='Warehouse No:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=2, column=0)
WhSubmit=Button(WarehouseFrame,text='Create Warehouse', command=createWharehouse, font=("Arial",12))
WhSubmit.grid(row=4, column=0)
WhUpdate=Button(WarehouseFrame,text='Update Warehouse', command=Updatewh, state=DISABLED,font=("Arial",12))
WhUpdate.grid(row=4, column=1, sticky=E)
sp=Label(WarehouseFrame, text=' ', bg='#C9DDFF').grid(row=3)
WhRes=Label(WarehouseFrame, text='', bg='#C9DDFF', font=("Arial",12))
WhRes.grid(row=5, column=0, columnspan=3)


whDef=Entry(WarehouseFrame, font=("Arial",12))
Wh_NoDef=Entry(WarehouseFrame, font=("Arial",12))
whDef.grid(sticky = W,row=1, column=1)
Wh_NoDef.grid(sticky = W,row=2, column=1)


typedef = StringVar()
typedef.set("Inbound")
vehicletypdef = StringVar()
vehicletypdef.set("Small")
Warehousedef = StringVar()
Warehousedef.set(WarehouseList[0])
Warehouse_Nodef = StringVar()
warehousehNolist(1)
Warehouse_Nodef.set(WarehouseNoList[0])
Warehousedef.trace("w", changewh)

def createwhno():
    global Warehouse_NoDef
    Warehouse_NoDef=OptionMenu(ansFrame, Warehouse_Nodef, *WarehouseNoList)
    Warehouse_NoDef.grid(sticky = W,row=4, column=1)
def createwarehouses():
    warehouseListCreate()
    global WarehouseDefs
    WarehouseDefs=OptionMenu(ansFrame, Warehousedef, *WarehouseList)
    WarehouseDefs.grid(sticky = W,row=3, column=1)
def createwarehousesrf():
    WarehouseDefs.destroy()
    createwarehouses()
Type=Label(ansFrame, text='Type:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=0, column=0)
Vehicle_Type=Label(ansFrame, text='Vehicle Type:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=1, column=0)
Vehicle_No=Label(ansFrame, text='Vehicle No:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=2, column=0)
Warehouse=Label(ansFrame, text='Warehouse:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=3, column=0)
Warehouse_No=Label(ansFrame, text='Warehouse No:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=4, column=0)
Exp_Date=Label(ansFrame, text='Exp. Arrival Date:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=5, column=0)
Exp_Time=Label(ansFrame, text='Exp. Arrival Time:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=6, column=0)
Shipping=Label(ansFrame, text='Shipping Details:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=7, column=0)

createwhno()
createwarehouses()
TypeDef=OptionMenu(ansFrame, typedef, "Inbound", "Outbound")
Vehicle_TypeDef=OptionMenu(ansFrame, vehicletypdef, "Small", "Medium", "Large", "Extra Large")
Vehicle_NoDef=Entry(ansFrame, font=("Arial",12))
Exp_DateDef=Entry(ansFrame, font=("Arial",12))
Exp_TimeDef=Entry(ansFrame, font=("Arial",12))
ShippingDef=Text(ansFrame, width=52, height=5, font=("Arial",12))

TypeDef.grid(sticky = W,row=0, column=1)
Vehicle_TypeDef.grid(sticky = W,row=1, column=1)
Vehicle_NoDef.grid(sticky = W,row=2, column=1)
Exp_DateDef.grid(sticky = W,row=5, column=1)
Exp_TimeDef.grid(sticky = W,row=6, column=1)
ShippingDef.grid(sticky = W,row=7, column=1)
sp=Label(ansFrame, text=' ').grid(row=11)
Submit=Button(ansFrame,text='Create ASN', command=createAns, font=("Arial",12)).grid(row=12, column=0, columnspan=2)
sp=Label(ansFrame, text=' ').grid(row=13)
Responce = Label(ansFrame, text='', bg='#C9DDFF', font=("Arial",12, BOLD))
Responce.grid(sticky = W,row=14, column=0,  columnspan=3)

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
        ShippingData.config(text = '-')
        OperationData.config(text = '-')
        ExpDateData.config(text = '-')
        ExpTimeData.config(text = '-')
        ActionData.config(state=DISABLED)
    else:
        for data in records:
            idData.config(text = data[0])
            VehicleTypeData.config(text = data[1])
            vehicleNoData.config(text = data[2])
            WarehouseData.config(text = data[3])
            WarehouseNoData.config(text = data[4])
            ShippingData.config(text = data[9])
            OperationData.config(text = data[10])
            ExpDateData.config(text = data[5])
            ExpTimeData.config(text = data[6])
            ActionData.config(state=NORMAL)
            global iddata
            iddata = data[0]
    sql = "SELECT Status FROM Stock WHERE id ='{}'".format(ansSearch.get())
    cursor.execute(sql)
    records = cursor.fetchall()
    if not cursor.rowcount:
        StatusData.config(text = '-')
    else:
        for data in records:
            StatusData.config(text = data[0])
    mysqldb.close()

def deleteANS():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my_password",
    database="testWMS"
    )

    cursor = mydb.cursor()

    sql = "DELETE FROM ANS WHERE id={};".format(iddata)
    cursor.execute(sql)
    mydb.commit()
    sql = "DELETE FROM Stock WHERE id={};".format(iddata)
    cursor.execute(sql)
    mydb.commit()
    mydb.close
    ANSResponce.config(text='ID: {} ASN is cancelled.'.format(iddata))

ansLabel=Label(ansSearchFrame, text='ANS Id:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(row=0, column=0)
ansSearch=Entry(ansSearchFrame)
sp1=Label(ansSearchFrame, text='  ', bg='#C9DDFF').grid(row=0, column=3)
submit=Button(ansSearchFrame, text='Fetch Details', font=("Arial",10, BOLD), command=fetchAns).grid(row=0, column=4)

sp2=Label(ansSearchFrame, text='  ', bg='#C9DDFF').grid(row=1)
sp3=Label(ansSearchFrame, text='  ', bg='#C9DDFF').grid(row=2)

id=Label(ansSearchFrame, text='ANS Id:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=3, column=0)
VehicleType=Label(ansSearchFrame, text='Vehicle Type:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=4, column=0)
vehicleNo=Label(ansSearchFrame, text='Vehicle No.:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=5, column=0)
Warehouse=Label(ansSearchFrame, text='Warehouse Name:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=6, column=0)
WarehouseNo=Label(ansSearchFrame, text='Warehouse No.:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=7, column=0)
Shipping=Label(ansSearchFrame, text='Shipping:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=8, column=0)
Operation=Label(ansSearchFrame, text='Operation:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=9, column=0)
ExpDate=Label(ansSearchFrame, text='Expected Date:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=10, column=0)
ExpTime=Label(ansSearchFrame, text='Expected Time:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=11, column=0)
Status=Label(ansSearchFrame, text='Status:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=12, column=0)
Action=Label(ansSearchFrame, text='Action:  ', bg='#C9DDFF', font=("Arial",12, BOLD)).grid(sticky = W,row=13, column=0)
ANSResponce=Label(ansSearchFrame, text='', bg='#C9DDFF', font=("Arial",12))
ANSResponce.grid(sticky = W,row=14, column=0)

idData=Label(ansSearchFrame, bg='#C9DDFF', font=("Arial",12))
VehicleTypeData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
vehicleNoData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
WarehouseNoData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
ShippingData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
OperationData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
ExpDateData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
ExpTimeData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
StatusData=Label(ansSearchFrame, text='-', bg='#C9DDFF', font=("Arial",12))
ActionData=Button(ansSearchFrame, text='Cancel', command=deleteANS, state=DISABLED, font=("Arial",12))

ansSearch.grid(sticky = W,row=0, column=1)
idData.grid(sticky = W,row=3, column=1)
VehicleTypeData.grid(sticky = W,row=4, column=1)
vehicleNoData.grid(sticky = W,row=5, column=1)
WarehouseData.grid(sticky = W,row=6, column=1)
WarehouseNoData.grid(sticky = W,row=7, column=1)
ShippingData.grid(sticky = W,row=8, column=1)
OperationData.grid(sticky = W,row=9, column=1)
ExpDateData.grid(sticky = W,row=10, column=1)
ExpTimeData.grid(sticky = W,row=11, column=1)
StatusData.grid(sticky = W,row=12, column=1)
ActionData.grid(sticky = W,row=13, column=1)
root.mainloop()
