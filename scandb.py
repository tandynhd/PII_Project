import sqlite3, csv
import os

print("Converting .db -> .csv ...")
####################################################################Adding data in .db
# conn = sqlite3.connect(location+'/test.db')
# c = conn.cursor()
# def create_table():
#     c.execute('CREATE TABLE IF NOT EXISTS hima(name TEXT, dob TEXT, pport TEXT, phone TEXT, email TEXT, address TEXT)')
# def data_entry():
#     c.execute("INSERT INTO employees VALUES('Bill', '12/07/2009', 'FA1254846', '993-992-9934', 'ss2313ff@gmail.com','UK')")
#     conn.commit()
#     c.close()
#     conn.close()
# create_table()
# data_entry()
##############################################################################

location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files/db'

onlyfiles = next(os.walk(location))[2]

data_source=[]

def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str

for index in range(len(onlyfiles)):
    conn = sqlite3.connect('C:/Users/Tandin Dorji/Desktop/PII_Project/files/db/'+onlyfiles[index])
    data_source.append(onlyfiles[index])
    c = conn.cursor()
    
    #list all the tables in the db
    def show_tables():
        c.execute("SELECT name FROM sqlite_master where type='table';")
        data = c.fetchall()
        for i in range(len(data)):
            a=data[i]
            b = convertTuple(a)
            read_from_db(b)

    def read_from_db(table):
        c.execute('SELECT * FROM {0}'.format(table))
        data = c.fetchall()
        with open(location+"/scan/Mock_report({0}_{1}).csv".format(onlyfiles[index],table), "w") as file:
            for row in data:
                csv.writer(file).writerow(row)

    show_tables()
    c.close
    del c
    conn.close()

print(data_source)
print('[complete]')

##################################################################################
##################################################################################

from pandas import *
from presidio_analyzer.analyzer_engine import AnalyzerEngine
import customreg

engine = AnalyzerEngine()
print('Scanning for PII data...')

engine.registry.add_recognizer(customreg.Th_passport_recognizer())
engine.registry.add_recognizer(customreg.Th_phone_recognizer())
engine.registry.add_recognizer(customreg.Th_ID_recognizer())

APP_FOLDER = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files/db/scan'

onlyfiles = next(os.walk(APP_FOLDER))[2] #dir is your directory path as string

#text = 'citizen id  083-0174456 AA1254846 1-2001-01756-87-5'
df = read_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/files/db/scan/'+onlyfiles[0]) 
columns = list(df)
pii_inventory = []
#d=[]
pii_categories =[]
data_source=[]
pii_type = []
for i in range(len(onlyfiles)):
    if ((onlyfiles[i][-5:]) != '.xlsx'):
        if (os.stat(APP_FOLDER +'/'+onlyfiles[i]).st_size) == 0:
            continue
        df = read_csv(APP_FOLDER +'/'+onlyfiles[i])
        for col in columns: 
            for index in df.index: 
                response = engine.analyze(correlation_id=0,
                                        text = str(df[col][index]),
                                        entities=[],language='en',
                                        #all_fields=True,
                                        score_threshold=0.6,)
                if (response != []):
                    pii_inventory.append({'type': response[0].entity_type,
                    'context':str(df[col][index]),
                    'position': "col: {}, row: {}".format(col,index),
                    'confidence': response[0].score,
                    'File': onlyfiles[i]})
    elif ((onlyfiles[i][-4:]) != '.csv'): 
        df = read_excel(APP_FOLDER +'/'+onlyfiles[i])
        for col in columns: 
            for index in df.index: 
                response = engine.analyze(correlation_id=0,
                                        text = str(df[col][index]),
                                        entities=[],language='en',
                                        #all_fields=True,
                                        score_threshold=0.6,)
                if (response != []):
                    pii_inventory.append({'type': response[0].entity_type,
                    'context':str(df[col][index]),
                    'position': "col: {}, row: {}".format(col,index),
                    'confidence': response[0].score,
                    'File': onlyfiles[i]})
    
    data_source.append(onlyfiles[i])        
report = DataFrame(pii_inventory)

report.to_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/files/report/mock_report(db).csv')

print(data_source)
print('[complete]')
