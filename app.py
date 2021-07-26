from test import PII_Data
from flask import Flask, render_template, request, redirect, url_for
import os, csv
from pandas import *

from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import urllib.request
import os

from pandas.io.formats.format import IntArrayFormatter

app = Flask(__name__)

@app.route('/')
def index():
    location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/report'

    onlyfiles = next(os.walk(location))[2]
    PII_Data = []
    for i in range(len(onlyfiles)):
        file = open("C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/report/"+onlyfiles[i])
        reader = csv.reader(file)
        lines = len(list(reader))
        PII_Data.append("There are "+str(lines-1)+" PII data in "+onlyfiles[i])
    return render_template('index.html', data=PII_Data)

app.config["FILE_UPLOADS"] = "C:/Users/Tandin Dorji/Desktop/PII_Project/Mock"
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

                report.to_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/html/Mock_report(html).csv')

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