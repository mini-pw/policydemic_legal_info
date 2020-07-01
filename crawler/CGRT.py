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
    
#converting CgrtRecord instance to DB INPUT
def convertToDatabaseRecords(records):
    dataBaseRecords = []    
    #TODO specify the DB INPUT
    for r in records:
        dataBaseRecords.append(None)
        
    return dataBaseRecords