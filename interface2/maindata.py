import sqlite3
from datetime import datetime

conn = sqlite3.connect('../maindata.db')

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER
             (USERID INT PRIMARYKEY NOT NULL,
              ADDRESS CHAR(50) NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              AADHAR CHAR(140) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
             );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS PRODUCE
             (ID INT PRIMARYKEY NOT NULL,
              FARMERUSERID INT NOT NULL,
              NAME CHAR(20) NOT NULL,
              TYPE CHAR(20) NOT NULL,
              QUANTITY INT NOT NULL,
              COST INT NOT NULL,
              SOLD BOOLEAN NOT NULL,
              DESCRIPTION CHAR(140) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              QUALITY_REVIEW INT,
              NO_TIMES_BOUGHT INT NOT NULL,
              FOREIGN KEY (FARMERUSERID) REFERENCES FARMER (USERID)
              );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS BUYER
             (BUYERID INT PRIMARYKEY NOT NULL,
              ADDRESS CHAR(50) NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              AADHAR CHAR(140) NOT NULL,
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
             );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS QUALITY_REVIEW
             (ID INT PRIMARYKEY NOT NULL,
              BUYERID INT NOT NULL,
              PRODUCEID INT NOT NULL,
              RATING INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (ID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit()


conn.execute('''CREATE TABLE IF NOT EXISTS BUSSINESS_HISTORY
             (ID INT PRIMARYKEY NOT NULL,
              BUYERID INT  NOT NULL,
              PRODUCEID INT NOT NULL,
              NAME CHAR(20) NOT NULL,
              TYPE CHAR(20) NOT NULL,
              QUANTITY INT NOT NULL,
              COST INT NOT NULL,
              DATE CHAR(12) NOT NULL,
              TIME CHAR(10) NOT NULL,
              FOREIGN KEY (PRODUCEID) REFERENCES PRODUCE (ID),
              FOREIGN KEY (BUYERID) REFERENCES BUYER (BUYERID)
              );'''
            )
conn.commit()


conn.close()
