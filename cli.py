# Helper file for testing queues
from pdfparser.tasks import pdfparser
from nlpengine.tasks import dispatch as nlpdispatch

import json

pdfparser.delay()
print("Done!")

# Testing Celery with Elasticsearch
with open('elastic/example-document.json') as jsonfd:
    doc_body = json.load(jsonfd)
nlpdispatch.delay(doc_body)
