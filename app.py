# from test import PII_Data
from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from pandas import *

from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import urllib.request
import os

from pandas.io.formats.format import IntArrayFormatter

app = Flask(__name__)

location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/'

if not os.path.exists(location+"files"):
    os.mkdir(location+"files")
if not os.path.exists(location+"files/csv"):
    os.mkdir(location+"files/csv")
if not os.path.exists(location+"files/db"):
    os.mkdir(location+"files/db")
if not os.path.exists(location+"files/doc"):
    os.mkdir(location+"files/doc")
if not os.path.exists(location+"files/pdf"):
    os.mkdir(location+"files/pdf")
if not os.path.exists(location+"files/report"):
    os.mkdir(location+"files/report")
if not os.path.exists(location+"files/txt"):
    os.mkdir(location+"files/txt")
if not os.path.exists(location+"files/html"):
    os.mkdir(location+"files/html")

@app.route('/')
def index():
    #location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/files'

    onlyfiles = next(os.walk(location+"/files/report"))[2]
    PII_Data = []
    for i in range(len(onlyfiles)):
        file = open(location+"/files/report/"+onlyfiles[i])
        reader = csv.reader(file)
        lines = len(list(reader))
        if (lines-1) == 1:
            PII_Data.append("There is 1 PII in "+onlyfiles[i])
        elif (lines-1) == 0:
            PII_Data.append("There is no PII in "+onlyfiles[i])
        else:
            PII_Data.append("There are "+str(lines-1)+" PII in "+onlyfiles[i])
    return render_template('index.html',len=len(PII_Data), data=PII_Data)

app.config["FILE_UPLOADS"] = location+"/files"
app.config["FILE_EXTENSIONS"] = ["CSV", "XLSX", "DB", "DOCX", "DOC", "PDF", "TXT"]

def allowed_files(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if request.files:           
            #scanweb
            weblink = request.form["web-scan"]
            if weblink != "":
                url=weblink
            
                print("Converting Website -> .csv ...")
        
                list = []
                PII_Inventory = []

                def tag_visible(element):
                    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
                        return False
                    if isinstance(element, Comment):
                        return False
                    return True


                def text_from_html(body):
                    soup = BeautifulSoup(body, 'html.parser')
                    texts = soup.findAll(text=True)
                    visible_texts = filter(tag_visible, texts)
                    return u" ".join(t.strip() for t in visible_texts)

                html = urllib.request.urlopen(url).read()

                list.append(text_from_html(html))
                text = list[0]
                info = text.split(" ")
                PII_Inventory.append(info)

                report = pd.DataFrame(PII_Inventory)

                report.to_csv(location+'/files/html/Mock_report(html).csv')

                print('[complete]')
                os.system("python scanweb.py")

            #scanfiles
            else:
                # test = request.files["file"]
                for file in request.files.getlist('file'):
                    if not allowed_files(file.filename):
                        print(file.filename+" has an unsupported extension")
                        continue
                    else:                    
                        file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
                        print("file saved: "+file.filename)
                os.system("python main.py")

        return redirect("http://127.0.0.1:5000/")  
    return render_template('upload.html')


@app.route('/report')
def piiView():
    return render_template('report.html')

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)