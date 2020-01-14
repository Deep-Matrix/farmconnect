import sqlite3
from datetime import datetime

conn = sqlite3.connect('../datahouse.db')

conn.execute('''CREATE TABLE IF NOT EXISTS TYPES
              (TYPEID INT PRIMARY KEY NOT NULL,
              TYPENAME CHAR(50) NOT NULL,
              TOTALAVAILABILITY INT
              );
        '''
        )
conn.commit() # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER
             (FARMERID INT PRIMARYKEY NOT NULL,
              ADDRESS CHAR(50) NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              AADHAR CHAR(140) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
             );'''
            )
conn.commit() # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS PRODUCE
            (
              PRODUCEID INT PRIMARY KEY NOT NULL,
              FARMERID INT NOT NULL,
              TYPEID INT NOT NULL,
              QUANTITY INT,
              COST INT,
              FOREIGN KEY (FARMERID) REFERENCES FARMER (FARMERID),
              FOREIGN KEY (TYPEID) REFERENCES TYPES(TYPEID)
            );'''
          )
conn.commit(); # Checked. OK

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER_PRODUCE
             (PRODUCEID INT NOT NULL,
              FARMERUSERID INT NOT NULL,
              QUANTITY INT NOT NULL,
              SOLD BOOLEAN NOT NULL,
              DESCRIPTION CHAR(140) NOT NULL,
              QUALITY_REVIEW INT,
              NO_TIMES_BOUGHT INT NOT NULL,
              FOREIGN KEY (FARMERUSERID) REFERENCES FARMER (FARMERID)
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (PRODUCEID)
              );'''
            ) # Checked. OK
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS BUYER
             (BUYERID INT PRIMARYKEY NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
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
