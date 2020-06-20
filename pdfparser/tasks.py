from scheduler.celery import app
import pytesseract
from PIL import Image
from wand.image import Image as wi

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