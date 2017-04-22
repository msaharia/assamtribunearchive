#!/usr/bin/python3

from bs4 import BeautifulSoup #For parsing the website
import requests 
import os 
import glob #For processing the downloaded JPG files 
from fpdf import FPDF #For working with PDFs
from datetime import datetime #For naming the exported PDF file
import pytz #For accounting for Indian Time Zone in the file name
import re
import sys

def functToDeleteItems(fullPathToDir):
   for itemsInDir in os.listdir(fullPathToDir):
        if os.path.isdir(os.path.join(fullPathToDir, itemsInDir)):
            functToDeleteItems(os.path.isdir(os.path.join(fullPathToDir, itemsInDir)))
        else:
            os.remove(os.path.join(fullPathToDir,itemsInDir))

def get_todays_homepage_url(url):
    """Gives the homepage URL to today's e-paper
    """
    r = requests.get(url)
    c = r.content #HTML content
    soup = BeautifulSoup(c,'lxml') #Making HTML content legible
    soup.find_all('meta')
    content = soup.select_one("meta[content*=url]")["content"]
    url = content.split(";")[-1].split("url=")[-1]
    sp = url.split('?') #Splittin the URL to what I need
    dailyurl = '/'.join(sp[0].split('/')[:4])+'/at.asp?'+sp[1]+'/'
    return dailyurl

def natural_sort(l):
    """Sorts by natural order of numbers
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def get_all_image_links(dailyurl):
    """Collates URLs of all images
    """
    r2 = requests.get(dailyurl)
    c2 = r2.content
    soup2 = BeautifulSoup(c2, 'lxml')
    #Storing all the Page URLs
    pageLinks = []
    imageLinks = []
    for anchor in soup2.find_all('a', {"class" : "PTopLink"}, href=True):
        pageLinks.append('http://www.assamtribune.com/scripts/'+ anchor['href'])
        imageLinks.append(os.path.join('http://www.assamtribune.com/scripts/spat.'+
        re.split('/|\.|=', anchor['href'])[1] + "=" + datetime.now().strftime("%Y"),
        re.split('/|\.|=', anchor['href'])[2], 
        'Big'+re.split('/|\.|=', anchor['href'])[3]+'.jpg'))        
    return imageLinks


def download_all_images(imageLinks):
    """Downloads all the images in full res
    """
    for image in imageLinks:
        r3 =requests.get(image,stream=True)
        soup3 = BeautifulSoup(r3.text,"lxml")
        img_link = soup3.find_all("img")
        download_url = "http://www.assamtribune.com"
        for link in img_link:
            download_url+=link["src"][2:]
            break
        r4 = requests.get(download_url, stream=True)
        if r4.status_code == 200:
            with open(os.path.normpath(os.getcwd() + os.sep + os.pardir) + "/img/" + re.findall('\d+', image)[2]+".jpg", 'wb') as f:
                f.write(r4.content)
	
def convert_images_to_pdf(imagelist, pdftitle, pdfcreator):
    """Convert all images to PDF. 
    imagelist is the list with all image filenames.
    """
    pdf = FPDF()
    for image in imagelist:
        pdf.add_page()
        pdf.image(image, w=170)
        pdf.set_title(pdftitle)
        pdf.set_creator(pdfcreator)
    at_filedate = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y%m%d")
    suffix = 'pdf'    
    at_filename = os.path.join(os.path.normpath(os.getcwd() + os.sep + os.pardir), 'pdf', at_filedate + "_assamtribune" + os.extsep + suffix)
    pdf.output(at_filename, "F")


def main():
    """One function to rule them all.
    """
    imd = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir, "img")) #Getting the directory of existing images
    functToDeleteItems(imd) #Deleting existing images
    y = get_todays_homepage_url("http://www.assamtribune.com/")
    z = get_all_image_links(y)
    download_all_images(z) #Download today's images
    imagelist = natural_sort(glob.glob('../img/*.jpg'))
    convert_images_to_pdf(imagelist, 'Assam Tribune Daily', 'Manabendra Saharia')

if __name__ == '__main__':
    sys.exit(main())
