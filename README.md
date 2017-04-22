# Assam Tribune Archive v0.2
![The Assam Tribune Logo](logo.png)

The [Assam Tribune](http://assamtribune.com) is the largest English language daily of North-East India. But the website is prehistoric with no proper archival system.

v0.2 script scrapes images of Assam Tribune daily and converts in into a single PDF for archival.

Very crude code. Patches are welcome. 

# Installation

    pip install --upgrade -r requirements.txt
    python3 src/atscraper.py

Set up Chron job to run everyday at 5:00 US CDT

    00 5 * * * cd full_path_to_src_folder && ./atscraper.py

# To be implemented in the future if time permits

* Optimize the file size of the PDF
* Integration with mailchimp for daily inbox delivery
* Downloading old editions of the paper
* OCR the images for a search database


