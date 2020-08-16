import unittest
import requests
from crawler.cgrt import CGRT

class CgrtTest(unittest.TestCase):
    #check if the link is correct and the response is ok
    def testCheckLink(self):
        r = requests.get(CGRT.URL, stream=True)
        self.assertEqual(r.ok, True)
    
    #download one record and check if it is filled
    def testDownloadOneRecord(self):
        records = CGRT.downloadCgrtRecords("Poland", "20200601", "20200601")
        
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].Country, "Poland")
        self.assertEqual(records[0].Date, "20200601")
        self.assertEqual(len(records[0].Data), 8)
        
    #check if five records are downloaded when the 5 dates are specified
    def testDownloadFiveRecords(self):
        records = CGRT.downloadCgrtRecords("Angola", "20200601", "20200605")
        self.assertEqual(len(records), 5)
    
    #check if nothing is downloaded when start date is bigger than end date
    def testCheckDateSwap(self):
        records = CGRT.downloadCgrtRecords("Angola", "20200605", "20200601")
        self.assertEqual(len(records), 0)
        
    #check if country is misspeled, nothing is returned   
    def testMisspeledCountry(self):
        records = CGRT.downloadCgrtRecords("Proland", "20200601", "20200601")
        self.assertEqual(len(records), 0)
            
if __name__ == '__main__':
   unittest.main()