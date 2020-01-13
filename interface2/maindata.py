import sqlite3

conn = sqlite3.connect('maindata.db')

conn.execute('''CREATE TABLE IF NOT EXISTS FARMER
             (USERID INT PRIMARYKEY NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              AADHAR CHAR(140) NOT NULL,  
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
             );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS PRODUCE
             (FARMERUSERID INT PRIMARYKEY NOT NULL,
              NAME CHAR(20) NOT NULL,
              TYPE CHAR(20) NOT NULL,
              QUANTITIY INT NOT NULL,               
              COST INT NOT NULL,
              SOLD BOOLEAN NOT NULL,
              FIELD CHAR(140) NOT NULL,  
              IMAGELINK CHAR(100) NOT NULL,
              QUALITY_REVIEW INT,
              );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS BUYER
             (BUYERID INT PRIMARYKEY NOT NULL,
              FULLNAME CHAR(20) NOT NULL,
              AADHAR CHAR(140) NOT NULL,  
              IMAGELINK CHAR(100) NOT NULL,
              DATEJOINED CHAR(12) NOT NULL,
              PHONENUMBER INT NOT NULL
             );'''
            )
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS QUALITY_REVIEW
             (BUYERID INT PRIMARYKEY NOT NULL,
              PRODUCEID INT NOT NULL,
              RATING INT
              );'''
            )
conn.commit()


conn.execute('''CREATE TABLE IF NOT EXISTS BUSSINESS_HISTORY
             (BUYERID INT PRIMARYKEY NOT NULL,
              PRODUCEID INT NOT NULL,
              NAME CHAR(20) NOT NULL,
              TYPE CHAR(20) NOT NULL,
              QUANTITIY INT NOT NULL,               
              COST INT NOT NULL,
              );'''
            )
conn.commit()


conn.close()