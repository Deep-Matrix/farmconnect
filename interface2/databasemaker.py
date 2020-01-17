import sqlite3
from datetime import datetime


# https://www.lucidchart.com/invitations/accept/d3788697-7d69-4a7a-91b5-88ae39a52165

conn = sqlite3.connect('datahouse.db')

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER
            (FARMERID CHAR(500) PRIMARY KEY NOT NULL,
              ADDRESS CHAR(50) NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              PASSWORD CHAR(50) NOT NULL,
              AADHAR CHAR(140) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
            );'''
            )
conn.commit() # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER_PRODUCE
            (PRODUCEID CHAR(500) PRIMARY KEY NOT NULL,
              FARMERUSERID CHAR(500) NOT NULL,
              QUANTITY INT NOT NULL,
              AVAILABLEQUANTITY INT NOT NULL,
              COST INT,
              SOLD BOOLEAN NOT NULL,
              DESCRIPTION CHAR(140) NOT NULL,
              QUALITY_REVIEW INT,
              NO_TIMES_BOUGHT INT NOT NULL,
              FOREIGN KEY (FARMERUSERID) REFERENCES FARMER (FARMERID)
              );'''
            ) # Checked. OK
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS BUYER
            (BUYERID CHAR(500) PRIMARY KEY NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              PASSWORD CHAR(50) NOT NULL,
              ADDRESS CHAR(150) NOT NULL,
              AADHAR CHAR(12) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
            );'''
            )
conn.commit() # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS QUALITY_REVIEW
            (ID INT CHAR(500) PRIMARY KEY NOT NULL,
              BUYERID CHAR(500) NOT NULL,
              PRODUCEID CHAR(500) NOT NULL,
              RATING INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (PRODUCEID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit() # Checked. OK


conn.execute('''CREATE TABLE IF NOT EXISTS BUSINESS_HISTORY
            (ID INT CHAR(500) PRIMARY KEY NOT NULL,
              BUYERID CHAR(500)  NOT NULL,
              PRODUCEID CHAR(500) NOT NULL,
              QUANTITY INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (PRODUCEID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS WAREHOUSE_OWNER
            (WAREHOUSE_OWNER_ID CHAR(500) PRIMARY KEY NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              PASSWORD CHAR(50) NOT NULL,
              ADDRESS CHAR(150) NOT NULL,
              AADHAR CHAR(12) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
            );'''
            )
conn.commit()


conn.execute('''CREATE TABLE  IF NOT EXISTS WAREHOUSE
            (WAREHOUSE_ID CHAR(500) PRIMARY KEY NOT NULL,
              OWNER_ID CHAR(500) NOT NULL,
              AVAILABLE_SIZE INT NOT NULL,
              PHOTO_URL CHAR(100) NOT NULL,
              LOCATION CHAR(200)  NOT NULL,
              COST INT NOT NULL,
              FOREIGN KEY (OWNER_ID) REFERENCES WAREHOUSE_OWNER(WAREHOUSE_OWNER_ID)
            );'''  
            )
conn.commit()


conn.execute('''CREATE TABLE  IF NOT EXISTS WAREHOUSE_TRANSACTION
            (TRANSACTION_ID CHAR(500) PRIMARY KEY NOT NULL,
              WAREHOUSE_ID CHAR(500) NOT NULL,
              FARMER_ID CHAR(200)  NOT NULL,
              PRODUCE_ID CHAR(500) NOT NULL,
              PRODUCE_QUANTITY INT NOT NULL,
              FOREIGN KEY (WAREHOUSE_ID) REFERENCES WAREHOUSE (ID),
              FOREIGN KEY (FARMER_ID) REFERENCES FARMER (FARMERID),
              FOREIGN KEY (PRODUCE_ID) REFERENCES FARMER_PRODUCE (PRODUCEID)
            );'''
            )
conn.commit()

conn.close()