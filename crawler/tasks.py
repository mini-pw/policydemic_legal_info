# from scheduler.celery import app
# from pdfparser.tasks import pdfparser

import requests 
from pathlib import Path

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
