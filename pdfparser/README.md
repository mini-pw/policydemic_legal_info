## PDF OCR
Before run ocr function install required packages, ImageMagick, ghostscript and Tesseract
### Python packages
```
pip install pytesseract
```
```
pip install wand
```
### ImageMagick
Download and install ImageMagick
http://docs.wand-py.org/en/latest/guide/install.html
### ghostscript
Download and install ghostscript
https://www.ghostscript.com/
### Tesseract
Download nad install Tesseract
https://github.com/tesseract-ocr/tessdoc/blob/master/Downloads.md
In pdfparser/config.py set path to tesseract. By default is r'/usr/bin/tesseract'.


## API

### Parse Function

```python
> parse(path)
```

Arguments:
* path - STRING - a path to a .pdf file

Return:
* STRING - the text of the chosen .pdf

"parse" task works as an endpoint. It takes a path of a pdf file as an argument and returns its text as a STRING.

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

### Check Function

```python
> check(pdf_text, keywords=set(), without=set(), at_least=1, at_most=1, crit="simple")
```
Arguments:
* pdf_text - STRING - the text of the .pdf document;
* keywords - SET of STRING - a python set of keywords;
* without - SET of STRING - a python set of words, that should not exist in pdf;
* at_least - INT - how many of the keywords should at least be in the text;
* at_most - INT - how many of the keywords should at most be in the text;
* crit - "simple" or "complex" - which criterion to choose.

Return:
* BOOL - True if the text fulfils the criterion

"check" task works as an endpoint. It takes a text of a pdf as a string and returns a boolean answer. It return True if the text fulfils the criterion. There is a simple criterion (crit = "simple") and complex criterion (crit = "complex"). Please notice, that the complex criterion is much slower.

Examples:

```python
> check("We're all mad here.", keywords={'mad'}, without=set(), at_least=1, at_most=1, crit="simple")
True
```

### Simple Criterion Function

```python
simple_crit(text, keywords, without=set(), at_least=1, at_most=1)
```

Arguments:
* text - STRING - the text of the .pdf document;
* keywords - SET of STRING - a python set of keywords;
* without - SET of STRING - a python set of words, that should not exist in pdf;
* at_least - INT - how many of the keywords should at least be in the text;
* at_most - INT - how many of the keywords should at most be in the text;

Return:
* BOOL - True if the text fulfils the criterion.

"simple_crit" checks if the intersection of set of words in the text and keywords set has at least "at_least" elements. If it has more than "at_most" words from the "without" set, it returns False.

Example:
```python
> simple_crit("Curiouser and curiouser!", {"curious"}, without=set(), at_least=1, at_most=1)
False

> simple_crit("Curiouser and curiouser!", {"curiouser"}, without=set(), at_least=1, at_most=1)
True
```

Note: Simple criterion is immune to uppercase/lowercase letters and punctuation marks.

### Complex Criterion Function

```python
complex_crit(text, keywords, without=set(), at_least=1, at_most=1, threshold=0.3)
```

Arguments:
* text - STRING - the text of the .pdf document;
* keywords - SET of STRING - a python set of keywords;
* without - SET of STRING - a python set of words, that should not exist in pdf;
* at_least - INT - how many of the keywords should at least be in the text;
* at_most - INT - how many of the keywords should at most be in the text;
* threshold - FLOAT - threshold for cosine distance. The smaller the more words the algorithm accepts as similar. Can be in range [-1,1].

Return:
* BOOL - True if the text fulfils the criterion.

"complex_crit" checks if the intersection of set of words in the text and keywords set has at least "at_least" elements. If it has more than "at_most" words from the "without" set, it returns False. However, the equivalency of two words is computed as follows: two words A and B get transformed into their embeddings, cosine is computed between those embeddings and if it is greater than "threshold", two words are equivalent.

Example:
```python
> text = "It would have made a dreadfully ugly child; but it makes rather a handsome pig.";

> keywords = {"toddler"};

> complex_crit(text, keywords)
True
```

The "complex_crit" returns True, because embeddings of the "toddler" word and the "child" word have a cosine greater than 0.3 and hence are equivalent.
