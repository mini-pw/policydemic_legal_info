# Crawler

This module is responsible from crawling PDFs from websites in domain `gov.pl`.
It contains 3 different crawlers:
* `GovDuSpider` - crawls pdfs created in year 2020 from website `dziennikustaw.gov.pl`.
The crawling process should last up to several minutes.
* `GovMpSpider` - crawls pdfs created in year 2020 from website `monitorpolski.gov.pl`.
The crawling process should last up to several minutes.
* `GovCrawler` - follows all website links starting from `gov.pl` and downloads found pdfs.
Link is classified as pdf whenever it contains `application/pdf` in response header under key `content-type`. 
The crawling process may last several hours using fixed search depth set to 100.
To visit even more websites, increase the value of `DEPTH_LIMIT` in `crawler.gov.gov.settings.py`

## CGRT Crawler

Crawler module have method `downloadCgrtData`, which gets the data from Coronavirus Government Response Tracker. The data is gathered in csv file, which contains significant number information about COVID-19.

Downloaded data is gathered into dictionary, which contains numbers describing information about:
* School closing
* Workplace closing
* Cancel public events
* Restrictions on gatherings
* Close public transport
* Stay at home requirements
* Restrictions on internal movement
* International travel controls

The parameters of `downloadCgrtData` function are the name of the country (in English), date from and date to. Inputed date should be of format "YYYYDDMM" (for example "20200721"). Each day is seperate downloaded record of data. 

## Downloading PDF file using URL

Crawler module contains `downloadPdf` function which downloads PDF file using specified URL. The parameters of the function are URL string, directory path (if does not exists, it will be created), name of downloaded PDF file and the size of the batch used in downloading in case of big files. Three last parameters have default values.
Function checks if the file under the URL have `application/pdf` value under key `content-type`, otherwise the file will not be downloaded.

* `PolicyWatchSpider`  crawls  governments' responses to the pandemic from website  `covid19policywatch.org`.

## Deployment
To start crawlers, simply import and start corresponding task:
```python
from crawler.tasks import crawl_gov_du
crawl_gov_du.delay()
```
For example, save above code in `cli.py` and start it with `python cli.py`.

## Automated tests
Tests for the `CGRT` module can be run (in a unix console) with:
```
PYTHONPATH=. python crawler/downloadTest.py
PYTHONPATH=. python crawler/cgrt/CgrtTest.py
```

## Future work
A possible extension of the scope of these crawlers may be too adjust them to documents which can be found starting from this url: https://www.dziennikiurzedowe.gov.pl/. 
