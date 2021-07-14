import sqlite3, csv

location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/db'

####################################################################Adding data in .db
# conn = sqlite3.connect(location+'/test.db')
# c = conn.cursor()

# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS employees(name TEXT, dob TEXT, pport TEXT, phone TEXT, email TEXT, address TEXT)')

# def data_entry():
#     c.execute("INSERT INTO employees VALUES('Bill', '12/07/2009', 'FA1254846', '993-992-9934', 'ss2313ff@gmail.com','UK')")
#     conn.commit()
#     c.close()
#     conn.close()

# create_table()
# data_entry()
##############################################################################

conn = sqlite3.connect(location+'/test.db')
c = conn.cursor()

def read_from_db():
    c.execute('SELECT * FROM employees')
    data = c.fetchall()
    print(data)
    with open(location+"/scan/Mock_report(db).csv", "w") as file:
        for row in data:
            csv.writer(file).writerow(row)

read_from_db()
c.close
del c
conn.close()




