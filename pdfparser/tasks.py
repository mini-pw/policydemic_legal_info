import PyPDF2
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBoxHorizontal

import collections

from scheduler.celery import app

# --- required for ocr --- #
import pytesseract
import io
from PIL import Image
from wand.image import Image as wi
from .config import ConfigOcr

# --- required for complex criterion --- #
import flair
from flair.embeddings import WordEmbeddings
import torch
import numpy as np
import pandas
from flair.data import Sentence

emb = WordEmbeddings('glove')


# -------------------------------------- #

@app.task
def pdfparser():
    print("Hello queue world!")


'''
Function return parsed text from pdf file using optical character recognition
path = path to pdf file
'''


@app.task
def pdfocr(path, lang='eng'):
    if len(path) == 0:
        print('Path is empty')
        return

    pytesseract.pytesseract.tesseract_cmd = ConfigOcr.path_to_tesseract
    pdf = wi(filename=path, resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    result_text = ""

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang=lang)
        result_text = result_text + text

    return result_text


# --------- Complex criterion --------- #
def cos(u, v):
    return u @ v / u.norm() / v.norm()


def complex_crit(text, keywords, without=set(), at_least=1, at_most=1, threshold=0.2):
    """
    Do common in a sense of embeddings exist?

    Text is a string.
    keywords is a set.
    without is a set.
    """

    t = Sentence(text)
    emb.embed(t)

    k = Sentence(" ".join(list(keywords)))
    emb.embed(k)

    if len(without):
        w = Sentence(" ".join(list(without)))
        emb.embed(w)

    ret_without = True
    ret_keywords = False
    for tt in t:
        if bool(without):
            for ww in w:
                if cos(tt.embedding, ww.embedding) > threshold:
                    at_most -= 1
                if at_most == 0:
                    ret_without = False
        for kk in k:
            if cos(tt.embedding, kk.embedding) > threshold:
                at_least -= 1
            if at_least == 0:
                ret_keywords = True

    return ret_without and ret_keywords


# ------------------------------------- #


# ---------- Simple criterion --------- #
def simple_crit(text, keywords, without=set(), at_least=1, at_most=1):
    """
    Do common words exist in keywords and text?

    Text is a string.
    keywords is a set.
    without is a set.
    """
    keywords = {k.lower() for k in keywords}

    lowered = text.lower()

    for m in ['.', ',', ':', ';', '-', '(', ')', '[', ']', '!', '?', '/', '\\']:
        lowered = lowered.replace(m, ' ')

    splitted = set(lowered.split())

    at_least_words = splitted.intersection(set(keywords))

    if len(at_least_words) > (at_least - 1):
        if bool(without):
            at_most_words = splitted.intersection(set(without))
            return len(at_most_words) <= (at_most - 1)
        else:
            return True
    else:
        return False


# ------------------------------------- #


# ----------  Parse function  --------- #
@app.task
def parse(path):
    empty_pages = []
    separated_text = []
    all_text = ""
    page_no = 0
    document = open(path, 'rb')
    pdf_info = PyPDF2.PdfFileReader(document).getDocumentInfo()
    pdf_metadata = {
        "author": pdf_info.author,
        "creator": pdf_info.creator,
        "producer": pdf_info.producer,
        "subject": pdf_info.subject,
        "title": pdf_info.title,
    }
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(document):
        text_on_page = []
        interpreter.process_page(page)
        layout = device.get_result()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                text_on_page.append(element.get_text())
                all_text+=element.get_text()
        if len(text_on_page) == 0:
            empty_pages.append(page_no)
        separated_text.append(text_on_page)
        page_no += 1
    document.close()
    return pdf_metadata, separated_text, empty_pages, all_text


# ------------------------------------- #


# ----------  Check function  --------- #
@app.task
def check(pdf_text, keywords=set(), without=set(), at_least=1, at_most=1, crit="simple"):
    crit = simple_crit if crit == "simple" else complex_crit
    return crit(pdf_text, keywords, without=without, at_least=at_least, at_most=at_most)


# ------------------------------------- #


# ----------  link processing --------- #
@app.task
def process_pdf_link(http_url):
    print(f"Received pdf: {http_url}")
# ------------------------------------- #
