import unittest
from crawler.tasks import downloadPdf
from os import path
import requests

testUrl = "http://zeszyty-naukowe.wwsi.edu.pl/zeszyty/zeszyt1/Algorytmy_Ewolucyjne_I_Ich_Zastosowania.pdf"

class TestTasks(unittest.TestCase):
    #test default file path
    def testDefaultDownloadFile(self):
        downloadPdf(testUrl)
        self.assertTrue(path.exists("./tmp/document.pdf"))
    
    #test specified file path
    def testSpecifiedDownloadFile(self):
        downloadPdf(testUrl, "testFolder", "testFile.pdf")
        self.assertTrue(path.exists("./testFolder/testFile.pdf"))
        
    #test if anything is written to output
    #should check the output for "File under this URL is not PDF"
    def testWrongUrl(self):
        downloadPdf("http://google.com")                                     
            


if __name__ == '__main__':
   unittest.main()