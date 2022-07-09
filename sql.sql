CREATE TABLE Stock (
    id int NOT NULL,
    Status varchar(50),
    Date varchar(10),
    Time varchar(10),
    Type varchar(10),
    PRIMARY KEY (Id)
);
CREATE TABLE ANS (
    id int NOT NULL AUTO_INCREMENT,
    Vehicle_Type varchar(50),
    vehicle_No varchar(20),
    Warehouse varchar(100),
    Warehouse_No int,
    Exp_Date varchar(10),
    Exp_Time varchar(10),
    Exp_Dep_Date varchar(10),
    Exp_Dep_Time varchar(10),
    Shipping varchar(255),
    Cr_Date varchar(10),
    Cr_Time varchar(10),
    PRIMARY KEY (Id)
);
CREATE TABLE Warehouse (
    id int NOT NULL AUTO_INCREMENT,
    WarehouseName varchar(100),
    Warehouse_No int,
    Date varchar(10),
    Time varchar(10),
    PRIMARY KEY (Id)
);
CREATE TABLE Login (
    id int NOT NULL AUTO_INCREMENT,
    WarehouseName varchar(100),
    Application varchar(20),
    Username varchar(10),
    Password varchar(10),
    PRIMARY KEY (Id)
);


INSERT INTO Warehouse (WarehouseName, Warehouse_No, Date, Time) VALUES ('Warehouse Jalandhar',2,'4/12/2021','10:00');
INSERT INTO Login (WarehouseName, Application, Username, Password) VALUES ('Warehouse Jalandhar','OUTBOUND','admin','admin');