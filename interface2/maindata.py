import sqlite3
from datetime import datetime


# https://www.lucidchart.com/invitations/accept/d3788697-7d69-4a7a-91b5-88ae39a52165

conn = sqlite3.connect('datahouse.db')

conn.execute('''CREATE TABLE IF NOT EXISTS TYPES
              (TYPEID INT PRIMARY KEY NOT NULL,
              TYPENAME CHAR(50) NOT NULL,
              TOTALAVAILABILITY INT
              );
        '''
        )
conn.commit() # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER
             (FARMERID INTEGER PRIMARY KEY NOT NULL,
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
             (PRODUCEID INTEGER PRIMARY KEY NOT NULL,
              FARMERUSERID INT NOT NULL,
              QUANTITY INT NOT NULL,
              AVAILABLEQUANTITY INT NOT NULL,
              SOLD BOOLEAN NOT NULL,
              DESCRIPTION CHAR(140) NOT NULL,
              QUALITY_REVIEW INT,
              NO_TIMES_BOUGHT INT NOT NULL,
              FOREIGN KEY (FARMERUSERID) REFERENCES FARMER (FARMERID)
              );'''
            ) # Checked. OK
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS BUYER
             (BUYERID INTEGER PRIMARY KEY NOT NULL,
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
             (ID INT PRIMARYKEY NOT NULL,
              BUYERID INT NOT NULL,
              PRODUCEID INT NOT NULL,
              RATING INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (PRODUCEID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit() # Checked. OK


conn.execute('''CREATE TABLE IF NOT EXISTS BUSINESS_HISTORY
             (ID INT PRIMARYKEY NOT NULL,
              BUYERID INT  NOT NULL,
              PRODUCEID INT NOT NULL,
              QUANTITY INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (PRODUCEID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit()

conn.close()
