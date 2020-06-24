# from scheduler.celery import app
# from pdfparser.tasks import pdfparser

import requests 
from pathlib import Path
import CGRT
import csv
import codecs

# @app.task
# def scan_website(link):
#     html = curl(link)
#     parsedhtml = parse(html)
#     # TODO get links from html
#     # add links to crawl QUEUE
#     for scrapped_link in scrapped_links:
#         scan_website.delay(scrapped_link)


# @app.task
# def crawl():
#     # TODO list of gov links
#     for link in gov_links:
#         if pdf:
#             pdfparser.delay(pdf)
#         else:
#             scan_website.delay(link)

#     print("Hello queue world!")


#download PDF file from url
@app.task
def downloadPdf(url, directory = 'tmp', filename = 'document.pdf', chunkSize = 1024):

    dirPath = Path(directory)
    #create directory if not exist
    dirPath.mkdir(parents=True, exist_ok=True)
    
    #send the request to specified url
    r = requests.get(url, stream = True)

    #reject if not PDF file    
    if 'application/pdf' not in r.headers.get('content-type'):
         print('File under this URL is not PDF')
         return
    
    fullPath = dirPath / filename
    #write to file
    with open(fullPath, "wb") as pdf:
        
        #write in chunks in case of big files 
        for chunk in r.iter_content(chunk_size = chunkSize): 
            
            # writing one chunk at a time to pdf file 
            if chunk: 
                pdf.write(chunk)



'''
function takes records from Coronavirus Government Response Tracker csv file
with specified country and date range 
date format is YYYYMMDD , for example "20200624"
'''
@app.task
def downloadCgrtData(country, dateFrom, dateTo):
    #list of records from csv file
    records = []
    #read the csv file from url
    r = requests.get(CGRT.URL, stream=True)
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
    for row in reader:
        #convert row from csv to class record
        record = CGRT.createCgrtRecord(row, country, dateFrom, dateTo)
        if record is None:
            continue
        records.append(record)
    
    #convert downloaded records to DB INPUT
    return CGRT.convertToDatabaseRecords(records)