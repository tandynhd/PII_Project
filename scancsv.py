from pandas import *
from presidio_analyzer.analyzer_engine import AnalyzerEngine
import customreg
import os
from datetime import datetime

engine = AnalyzerEngine()
print('Scanning for PII data...')

engine.registry.add_recognizer(customreg.Th_passport_recognizer())
engine.registry.add_recognizer(customreg.Th_phone_recognizer())
engine.registry.add_recognizer(customreg.Th_ID_recognizer())

APP_FOLDER = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files'

onlyfiles = next(os.walk(APP_FOLDER+'/csv'))[2] #dir is your directory path as string

#text = 'citizen id  083-0174456 AA1254846 1-2001-01756-87-5'
df = read_csv(APP_FOLDER+'/csv/'+onlyfiles[0]) 
columns = list(df)
pii_inventory = []
#d=[]
pii_categories =[]
data_source=[]
pii_type = []
for i in range(len(onlyfiles)):
    if ((onlyfiles[i][-4:]) == '.csv'):
        if (os.stat(APP_FOLDER +'/csv/'+onlyfiles[i]).st_size) == 0:
            continue
        df = read_csv(APP_FOLDER +'/csv/'+onlyfiles[i])
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
    elif ((onlyfiles[i][-5:]) == '.xlsx'):
        if (os.stat(APP_FOLDER +'/csv/'+onlyfiles[i]).st_size) == 0:
            continue
        df = read_excel(APP_FOLDER +'/csv/'+onlyfiles[i])
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

now = datetime.now()
current_time = now.strftime("dmy%d%m%y-hms%H%M%S")
report.to_csv(APP_FOLDER+'/report/csvreport({0}).csv'.format(current_time))

print(data_source)
print('[complete]')
