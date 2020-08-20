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

import textdistance

'''
Function return parsed text from pdf file using optical character recognition
path = path to pdf file
pages = pages to recognize
'''
@app.task
def pdfocr(path, pages=[], lang='eng'):
    """
    ### pdfocr Function

    ```python
    > pdfocr(path, pages=[], lang='eng')
    ```

    Arguments:
    * path - STRING - a path to a .pdf file;
    * pages - LIST<INT> - number of pages to recognize, empty if whole document
    * lang - STRING - language, english by default.

    Return:
    * LIST<STRING> - list of the text of the chosen .pdf pages

    The function returns parsed text from pdf file using OCR (optical character recognition). It takes a path of a pdf file as an argument and returns its text as a STRING.
    """

    if len(path) == 0:
        print('Path is empty')
        return

    pytesseract.pytesseract.tesseract_cmd = ConfigOcr.path_to_tesseract
    pdf = wi(filename=path, resolution=300)
    pdfImage = pdf.convert('jpeg')

    imageBlobs = []
    count = 1

    for img in pdfImage.sequence:
        if (not pages) or count in pages:
            imgPage = wi(image=img)
            imageBlobs.append(imgPage.make_blob('jpeg'))
        count = count + 1

    result_text = []

    for imgBlob in imageBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang=lang)
        result_text.append(text)

    return result_text

# --------- Complex criterion --------- #
def cos(u,v):
    return u.dot(v) / u.norm() / v.norm()
def embedding_cosine(str1, str2):
    s1 = Sentence(str1)
    emb.embed(s1)
    s2 = Sentence(str2)
    emb.embed(s2)

    return cos(s1[0].embedding, s2[0].embedding)

def complex_crit(text, keywords, without=set(), at_least=1, at_most=1, similarity="hamming", threshold=1):
    """
    complex_crit

    Arguments:
    * text - STRING - the text of the .pdf document;
    * keywords - SET of STRING - a python set of words, that should be in the text;
    * without - SET of STRING - a python set of words, that shouldn't be in the text;
    * at_least - INT - an integer indicating, how many unique words from of the keywords set should at least be in the text. If the number of words is smaller, function returns False;
    * at_most - INT - an integer indicating, how many of the keywords should at most be in the text. If the number is bigger, function returns False;

    * threshold - FLOAT - threshold for cosine distance. The smaller the more words the algorithm accepts as similar. Can be in range [-1,1].
    * similarity - textdistance algorithm or embedding_cosine - similarity algorithm. It can be from the textdistance package or embedding_cosine algorithm.

    Return:
    * BOOL - True if the text fulfils the criterion.

    "complex_crit" checks if the intersection of set of words in the text and keywords set has at least "at_least" elements. If it has more than "at_most" words from the "without" set, it returns False. However, we say that two words A and B are equivalent when their similarity is above "threshold". Similarity is any function, that takes two strings and returns real number, that expresses similarity between those words. There are several distances to choose from, including:
    * Embedding cosine similarity: two words A and B get transformed into their embeddings, cosine is computed between those embeddings and if it is greater than "threshold", two words are equivalent.
    * Hamming similarity: https://en.wikipedia.org/wiki/Hamming_distance
    * Levenshtein similarity: https://en.wikipedia.org/wiki/Levenshtein_distance

    and others from the textdistance package: https://pypi.org/project/textdistance/.


    Example:
    ```python
    > text = "It would have made a dreadfully ugly child; but it makes rather a handsome pig.";

    > keywords = {"toddler"};

    > complex_crit(text, keywords)
    True
    ```

    The "complex_crit" returns True, because embeddings of the "toddler" word and the "child" word have a cosine greater than 0.3 and hence are equivalent.
    """

    if type(similarity) == str:
        s = {
            "hamming": td.hamming.similarity,
            "levenshtein":td.levenshtein.similarity,
            "embedding":embedding_cosine,
            "embedding_cosine":embedding_cosine,
            "cosine":embedding_cosine
        }
        try:
            similarity = s[similarity]
        except:
            print("Similarity unknown. Please check your selected similarity measure.")


    # Keywords and without to lowercase
    keywords = {k.lower() for k in keywords}
    without = {w.lower() for w in without}
    # Lowered
    lowered = text.lower()
    # No punctuation
    for m in ['.', ',', ':', ';', '-', '(', ')', '[', ']', '!', '?', '/', '\\']:
        lowered = lowered.replace(m, ' ')
    # Split
    splitted = set(lowered.split())

    ret_without = True
    ret_keywords = False

    if bool(without):
        for ww in without:
            for tt in splitted:
                if similarity(tt, ww) >= threshold:
                    at_most -= 1
                    if at_most == 0:
                        ret_without = False
                    break

    for kk in keywords:
        for tt in splitted:
            if similarity(tt, kk) >= threshold:
                at_least -= 1
                if at_least == 0:
                    ret_keywords = True
                break

    return ret_without and ret_keywords
# ------------------------------------- #


# ---------- Simple criterion --------- #
def simple_crit(text, keywords, without=set(), at_least=1, at_most=1):
    """
    simple_crit

    Arguments:
    * text - STRING - the text of the .pdf document;
    * keywords - SET of STRING - a python set of words, that should be in the text;
    * without - SET of STRING - a python set of words, that shouldn't be in the text;
    * at_least - INT - an integer indicating, how many unique words from of the keywords set should at least be in the text. If the number of words is smaller, function returns False;
    * at_most - INT - an integer indicating, how many of the keywords should at most be in the text. If the number is bigger, function returns False;

    Return:
    * BOOL - True if the text fulfils the criterion, i.e. if it has at least "at_least" words from the keywords set and at most "at_most" words from the without set.

    "simple_crit" checks if the intersection of set of words in the text and keywords set has at least "at_least" elements. If it has more than "at_most" words from the "without" set, it returns False.

    Example:
    ```python
    > simple_crit("Curiouser and curiouser!", {"curious"}, without=set(), at_least=1)
    False

    > simple_crit("Curiouser and curiouser!", {"curiouser"}, without=set(), at_least=1)
    True
    ```

    Note: Simple criterion is immune to uppercase/lowercase letters and punctuation marks.
    """
    keywords = {k.lower() for k in keywords}
    without = {w.lower() for w in without}

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
    """
    parse

    Arguments:
    * path - STRING - a path to a single .pdf file;

    Return:
    * pdf_metadata, separated_text, empty_pages, all_text - TUPLE, where:
        * pdf_metadata - DICT containing metadata extracted from the parsed file. Contains the author, creator,
            producer, subject and title of the file in the respective keys in the dictionary.
        * separated_text - LIST of LISTS containing the text in the parsed file, separated into pages,
            and every page separated into paragraphs (blocks of texts). In the separated_text list, each element
            corresponds to one page of the document and each element of this element corresponds to one paragraph.
        * empty_pages - LIST of pages in the parsed file which did not contain any text. The list shall be used to
            run `pdfocr` function on the missing pages.
        * all_text - STRING containing the entire text of the parsed PDF file.

    "parse" task works as an endpoint. It takes a path of a pdf file as an argument and returns its metadata,
    its text in STRING format, LIST of unparsed pages as well as LIST of LISTS of text separated into pages
    and pages into paragraphs.
    """

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
def check(pdf_text, keywords=set(), without=set(), at_least=1, at_most=1, similarity="hamming", threshold=5, crit="simple"):
    """
    check

    Arguments:
    * text - STRING - the text of the .pdf document;
    * keywords - SET of STRING - a python set of words, that should be in the text;
    * without - SET of STRING - a python set of words, that shouldn't be in the text;
    * at_least - INT - an integer indicating, how many unique words from of the keywords set should at least be in the text. If the number of words is smaller, function returns False;
    * at_most - INT - an integer indicating, how many of the keywords should at most be in the text. If the number is bigger, function returns False;

    * threshold - FLOAT - threshold for cosine distance. The smaller the more words the algorithm accepts as similar. Can be in range [-1,1].
    * similarity - textdistance algorithm or embedding_cosine - similarity algorithm. It can be from the textdistance package or embedding_cosine algorithm.

    Return:
    * BOOL - True if the text fulfils the criterion.

    check is a bridge to simple_crit and complex crit function. For details please check their documentation.
    """
    if crit == "simple":
        return simple_cirt(pdf_text, keywords, without=without, at_least=at_least, at_most=at_most)
    else:
        return complex_crit(pdf_text, keywords, without=without, at_least=at_least, at_most=at_most, similarity=similarity, threshold=threshold)
# ------------------------------------- #

# ----------  link processing --------- #
@app.task
def process_pdf_link(http_url):
    print(f"Received pdf: {http_url}")
# ------------------------------------- #
