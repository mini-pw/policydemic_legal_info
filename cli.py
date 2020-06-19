# Helper file for testing queues
from pdfparser.tasks import pdfparser

pdfparser.delay()
print("Done!")
