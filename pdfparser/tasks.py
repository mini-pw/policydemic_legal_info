import PyPDF2

import collections

from scheduler.celery import app

import pytesseract
from PIL import Image
from wand.image import Image as wi

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

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #path to tesseract.exe
    pdf = wi(filename=path, resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []

    for img in pdfImage.sequence:
        imgPage = wi(image=img)
        imageBlobs.append(imgPage.make_blob('jpeg'))

    result_text = []

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang=lang)
        result_text.append(text)

    return result_text

# --------- Complex criterion --------- #
def cos(u,v):
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

    if len(at_least_words) > (at_least-1):
        if bool(without):
            at_most_words = splitted.intersection(set(without))
            return len(at_most_words) <= (at_most-1)
        else:
            return True
    else: return False
# ------------------------------------- #



# ----------  Parse function  --------- #
@app.task
def parse(path):
    pdf_text_list=[]
    with open(path, 'rb') as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        c = collections.Counter(range(number_of_pages))
        for i in c:
            page = read_pdf.getPage(i)
            page_content = page.extractText()
            pdf_text_list.append(page_content)
        pdf_file.close()

    pdf_text = " ".join(pdf_text_list)
    return pdf_text
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
