from scheduler.celery import app
from elasticsearch import Elasticsearch

es = Elasticsearch()


@app.task
def dispatch(document_body):
    print("Dummy consumption of body")

    index_document(document_body)


def index_document(body):
    """
    Stores a document in an Elasticsearch index, according to the structure

    :param body: document body (JSON-like)
    :return: response from Elasticsearch
    """
    es.index(
        index='documents',
        doc_type='document',
        body=body
    )
