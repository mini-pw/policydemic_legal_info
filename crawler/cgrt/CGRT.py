import json
from nlpengine.tasks import index_document
import requests
import csv
import codecs

#URL containing Coronavirus Government Response Tracker csv file
URL = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv'

#requested data columns from csv files
dataColumns = {
    'School closing' : 3,
    'Workplace closing' : 5,
    'Cancel public events' : 7,
    'Restrictions on gatherings' : 9,
    'Close public transport' : 11,
    'Stay at home requirements' : 13,
    'Restrictions on internal movement' : 15,
    'International travel controls' : 17
}

# class containing specified information from csv file record
class CgrtRecord:
    def __init__(self, country, date, data):
        self.Country = country
        self.Date = date
        self.Data = {}
        for key in dataColumns.keys():
            self.Data[key] = data[dataColumns[key]]

#function creating CgrtRecord instance basing on csv row with conditions
#if conditions are not fulfilled, None is returned
def createCgrtRecord(row, country, dateFrom, dateTo):
    if country == row[0] and dateFrom <= row[2] and dateTo >= row[2]:
        return CgrtRecord(row[0], row[2], row)
    else:
        return None

#function downloading csv info with specified criteria
def downloadCgrtRecords(country, dateFrom, dateTo):
    #list of records from csv file
    records = []
    #read the csv file from url
    r = requests.get(URL, stream=True)
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',')
    for row in reader:
        #convert row from csv to class record
        record = createCgrtRecord(row, country, dateFrom, dateTo)
        if record is None:
            continue
        records.append(record)
        
    return records

#send downloaded records to nlp engine
def saveIntoDatabase(records):
    for rec in records:
        rec.Data["Country"] = rec.Country
        rec.Data["Date"] = rec.Date
        jsonString = json.dumps(rec.Data)
        index_document(jsonString)