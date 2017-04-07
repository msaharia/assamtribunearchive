#!/usr/bin/env python

from bs4 import BeautifulSoup #For parsing the website
import requests 
import os 
import glob #For processing the downloaded JPG files 
from fpdf import FPDF #For working with PDFs
from datetime import datetime #For naming the exported PDF file
import pytz #For accounting for Indian Time Zone in the file name
import re
import erequests #For Asyncronous downloading of images

r = requests.get('http://www.assamtribune.com/') #Page Response
c = r.content #HTML content
soup = BeautifulSoup(c,'lxml') #Making HTML content legible

soup.find_all('meta')
content = soup.select_one("meta[content*=url]")["content"]
url = content.split(";")[-1].split("url=")[-1]
 
sp = url.split('?')

dailyurl = '/'.join(sp[0].split('/')[:4])+'/at.asp?'+sp[1]+'/'

r2 = requests.get(dailyurl)
c2 = r2.content
soup2 = BeautifulSoup(c2,'lxml')

#Storing all the Page URLs
pageLinks = []
imageLinks = []
imageLinks2 = []

for anchor in soup2.find_all('a', { "class" : "PTopLink" }, href=True): #Storing all URLs from HTML
     pageLinks.append('http://www.assamtribune.com/scripts/'+ anchor['href'])  
     imageLinks.append(os.path.join('http://www.assamtribune.com/scripts/spat.'+
                 re.split('/|\.|=', anchor['href'])[1] + "=" + datetime.now().strftime("%Y") ,
                 re.split('/|\.|=', anchor['href'])[2] , 
                 'Big'+re.split('/|\.|=', anchor['href'])[3]+'.jpg'))

rs = [erequests.async.get(u) for u in imageLinks]
list(erequests.map(rs))

# erequests.map will call each async request to the action
# what returns processed request `req`
for req in erequests.map(rs):
    if req.ok:
        content = req.content
        # process it here
        print(req.url)

#for image in imageLinks:
#    r3 =requests.get(image,stream=True)
#    soup3 = BeautifulSoup(r3.text,"lxml")
#    img_link = soup3.find_all("img")
#    download_url = "http://www.assamtribune.com"
#    for link in img_link:
#        download_url+=link["src"][2:]
#        break
#    r4 = requests.get(download_url, stream=True)
#    if r4.status_code == 200:
#        #with open(os.getcwd() + "/img/" + image.split("/")[-1], 'wb') as f:
#        with open(os.getcwd() + "/img/" + re.findall('\d+', image)[2]+".jpg", 'wb') as f:
#            f.write(r4.content)

#For sorting the pages by natural order

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

imagelist = natural_sort(glob.glob('img/*.jpg'))

#Coverting the images to PDF
pdf = FPDF()
# imagelist is the list with all image filenames
for image in imagelist:
    pdf.add_page()
    pdf.image(image, w=170)
    pdf.set_title('Assam Tribune Daily')
    pdf.set_creator('Manabendra Saharia')

at_filedate = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y%m%d")
suffix = 'pdf'    
at_filename = os.path.join(os.getcwd(), 'pdf', at_filedate + "_assamtribune" + os.extsep + suffix)

pdf.output(at_filename, "F")
