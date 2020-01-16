import sqlite3
import os
conn = sqlite3.connect(os.path.realpath('datahouse.db'))


conn.execute('''INSERT INTO FARMER(phonenumber, fullname, password, address, aadhar, imagelink, datejoined) VALUES
 (7021815984,  "Nimish Vithalani", "xyz123", "Andheri Road, Andheri", 989898989898, "t.com/sss.jpg", "2019-12-01");''')
conn.commit()