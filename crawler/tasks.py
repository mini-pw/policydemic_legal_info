import codecs
import csv
import os
from pathlib import Path

import requests
from billiard.context import Process
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from crawler import CGRT
from crawler.gov.gov.spiders.gov import GovDuSpider, GovCrawler, GovMpSpider
from scheduler.celery import app


class CrawlerProcess(Process):
    """ This class allows to run scrapy Crawlers using multiprocessing from billiard """

    def __init__(self, spider):
        Process.__init__(self)
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'crawler.gov.gov.settings')
        settings = get_project_settings()
        self.crawler = Crawler(spider.__class__, settings)
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        reactor.run()


@app.task
def crawl_gov_du():
    """ Starts crawling process which downloads pdfs from dziennikustaw.gov.pl """
    spider = GovDuSpider()
    process = CrawlerProcess(spider)
    process.start()
    process.join()


@app.task
def crawl_gov_mp():
    """ Starts crawling process which downloads pdfs from monitorpolski.gov.pl """
    spider = GovMpSpider()
    process = CrawlerProcess(spider)
    process.start()
    process.join()


@app.task
def crawl_gov():
    """ Starts crawling process which downloads pdfs from all websites in domain gov.pl """
    crawler = GovCrawler()
    process = CrawlerProcess(crawler)
    process.start()
    process.join()


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