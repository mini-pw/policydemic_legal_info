import os

from elasticsearch import Elasticsearch
from celery import chain
from celery.task import subtask
from configparser import ConfigParser
from datetime import datetime

from scheduler.celery import app
import crawler.tasks as crawler_tasks
import pdfparser.tasks as pdfparser_tasks
import translator.tasks as translator_tasks

config = ConfigParser()
config.read('nlpengine/config.ini')

es_hosts = config['elasticsearch']['hosts']
pdf_rootdir = config['pdf_database']['rootdir']
es = Elasticsearch(hosts=es_hosts)

INDEX_NAME = 'documents'
DOC_TYPE = '_doc'

SCRAP_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


@app.task
def process_pdf_link(pdf_url):
    print(f"Received pdf: {pdf_url}")

    pdf_chain = \
        download_pdf.s() | \
        parse_pdf.s() | \
        translate_pdf.s() | \
        process_document.s()

    pdf_chain(pdf_url)


@app.task
def download_pdf(pdf_url):
    pdf_filename = os.path.basename(pdf_url)
    pdf_path = os.path.join(pdf_rootdir, pdf_filename)

    crawler_tasks.downloadPdf.apply(kwargs={
        "url": pdf_url,
        "directory": pdf_rootdir,
        "filename": pdf_filename
    })

    return {
        "web_page": pdf_url,
        "pdf_path": pdf_path
    }


@app.task
def parse_pdf(body):
    pdf_path = body["pdf_path"]
    parse_result = pdfparser_tasks.parse(pdf_path)

    body.update({"original_text": parse_result})
    return body


@app.task
def translate_pdf(body):
    original_text = body["original_text"]
    result = translator_tasks.translate(original_text)

    body.update(result)
    return body


@app.task
def process_document(body):
    scrap_date = datetime.now().strftime(SCRAP_DATE_FORMAT)

    body.update({
        "document_type": "legalact",
        "scrap_date": scrap_date,
        "text_parsing_type": "parser",
        "keywords": []
    })
    index_document(body)


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
