from PyPDF2 import PdfFileReader

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
def complex_crit(text, key_words, without=set(), at_least=1, at_most=1, threshold=0.3):
    """
    Do common in a sense of embeddings exist?

    Text is a string.
    key_words is a set.
    without is a set.
    """

    t = Sentence(text)
    emb.embed(t)

    k = Sentence(" ".join(list(key_words)))
    emb.embed(k)

    if len(without):
        w = Sentence(" ".join(list(without)))
        emb.embed(w)

    for tt in t:
        for kk in k:
            if cos(tt.embedding, kk.embedding) > threshold:
                at_least -= 1
            if at_least == 0:
                return True
            if bool(without):
                if cos(tt.embedding, kk.embedding) > threshold:
                    at_most -= 1
                if at_most == 0:
                    return False
    return False
# ------------------------------------- #

# ---------- Simple criterion --------- #
def simple_crit(text, key_words, without=set(), at_least=1, at_most=1):
    """
    Do common words exist in key_words and text?

    Text is a string.
    key_words is a set.
    without is a set.
    """
    splitted = set(text.split())

    at_least_words = splitted.intersection(set(key_words))

    if len(at_least_words) > (at_least-1):
        if bool(without):
            at_most_words = splitted.intersection(set(without))
            return len(at_most_words) <= (at_most-1)
        else:
            return True
    else: return False
# ------------------------------------- #

@app.task
def parse(path, key_words=set(), without=set(), at_least=1, at_most=1, crit="simple"):
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
    if bool(key_words):
        return pdf_text_list
    else:
        crit = simple_crit if crit == "simple" else complex_crit
        return [t for t in pdf_text_list if crit(t, key_words, without=without, at_least=at_least, at_most=at_most)]

