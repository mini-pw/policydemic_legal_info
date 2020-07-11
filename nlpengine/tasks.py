from scheduler.celery import app
from elasticsearch import Elasticsearch
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

es_hosts = config['elasticsearch']['hosts']
es = Elasticsearch(hosts=es_hosts)

INDEX_NAME = 'documents'
DOC_TYPE = 'document'


@app.task
def insert_document(data):
    index_document(data)

@app.task
def modify_document(document_id, data):
    update_document(document_id, data)


def index_document(body):
    """
    Stores a document in Elasticsearch index, according to the structure

    :param body: document body (JSON-like)
    :return: response from Elasticsearch
    """
    es.index(
        index=INDEX_NAME,
        doc_type=DOC_TYPE,
        body=body
    )

def update_document(id, body):
    """
    Updates a document in Elasticsearch index, applying mentioned changes

    :param id: hash document ID 
    :param body: elements of body to update
    :return response from Elasticsearch
    """

    es.update(
        index=INDEX_NAME,
        doc_type=DOC_TYPE,
        id=id,
        body=body
    )