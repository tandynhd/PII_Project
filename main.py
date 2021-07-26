import os
import shutil
location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files/'
files = os.listdir(location)

for file in files:
    if (".xlsx") in file:
        shutil.move(location+file,location+"csv/"+file)
    elif (".csv") in file:
        shutil.move(location+file,location+"csv/"+file)
    elif (".db") in file:
        shutil.move(location+file,location+"db/"+file)
    elif (".docx") in file:
        shutil.move(location+file,location+"doc/"+file)
    elif (".doc") in file:
        shutil.move(location+file,location+"doc/"+file)
    elif (".pdf") in file:
        shutil.move(location+file,location+"pdf/"+file)
    elif (".txt") in file:
        shutil.move(location+file,location+"txt/"+file)
   
dir ='C:/Users/Tandin Dorji/Desktop/PII_Project/files/csv'
directory= os. listdir(dir)
if len(directory) != 0:
    os.system("python scancsv.py")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

dir ='C:/Users/Tandin Dorji/Desktop/PII_Project/files/doc'
directory= os. listdir(dir)
if len(directory) != 0:
    os.mkdir(dir+"/scan")
    os.system("python scandoc.py")
    shutil.rmtree(dir+"/scan")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

dir ='C:/Users/Tandin Dorji/Desktop/PII_Project/files/pdf'
directory= os. listdir(dir)
if len(directory) != 0:
    os.mkdir(dir+"/scan")
    os.system("python scanpdf.py")
    shutil.rmtree(dir+"/scan")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

dir ='C:/Users/Tandin Dorji/Desktop/PII_Project/files/txt'
directory= os. listdir(dir)
if len(directory) != 0:
    os.mkdir(dir+"/scan")
    os.system("python scantxt.py")
    shutil.rmtree(dir+"/scan")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

dir ='C:/Users/Tandin Dorji/Desktop/PII_Project/files/db'
directory= os. listdir(dir)
if len(directory) != 0:
    os.mkdir(dir+"/scan")
    os.system("python scandb.py")
    shutil.rmtree(dir+"/scan")
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


