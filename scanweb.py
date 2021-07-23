from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd
import urllib.request
import os

from pandas.io.formats.format import IntArrayFormatter

print("Converting Website -> .csv ...")
weblink = []
location = 'C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/html'
with open(location+"/weblink.txt", 'r+') as file:
    pageinfo = file.read()
    print(pageinfo)
    weblink.append(pageinfo)
    print(weblink)
url = weblink[0]
print(url)
#url = 'https://www.siit.tu.ac.th/academics_school.php?id=4&ssid=42'

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

report.to_csv('C:/Users/Tandin Dorji/Desktop/PII_Project/Mock/html/scan/Mock_report(html).csv')

print('[complete]')
os.system("python scanweb2.py")

