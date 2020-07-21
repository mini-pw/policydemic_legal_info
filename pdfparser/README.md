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
* path - STRING - a path to a single .pdf file;

Return:
* STRING - the text of the chosen .pdf;

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
> check(pdf_text, keywords=set(), without=set(), at_least=1, at_most=1, similarity="hamming", threshold=5, crit="simple")
```
Arguments:
* text - STRING - the text of the .pdf document;
* keywords - SET of STRING - a python set of words, that should be in the text;
* without - SET of STRING - a python set of words, that shouldn't be in the text;
* at_least - INT - an integer indicating, how many unique words from of the keywords set should at least be in the text. If the number of words is smaller, function returns False;
* at_most - INT - an integer indicating, how many of the keywords should at most be in the text. If the number is bigger, function returns False;

* threshold - FLOAT - threshold for similarity. The smaller the more words the algorithm accepts as similar.
* similarity - textdistance algorithm or embedding_cosine - similarity algorithm. It can be from the textdistance package or embedding_cosine algorithm.

Return:
* BOOL - True if the text fulfils the criterion.

check is a bridge to simple_crit and complex_crit function. For details please check their documentation.

"check" task works as an endpoint. It takes a text of a .pdf as a string and returns a boolean answer. It return True if the text fulfils the criterion. There is a simple criterion (crit = "simple") and complex criterion (crit = "complex"). Please notice, that the complex criterion is much slower.

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

### Complex Criterion Function

```python
complex_crit(text, keywords, without=set(), at_least=1, at_most=1, threshold=0.3)
```

Arguments:
* text - STRING - the text of the .pdf document;
* keywords - SET of STRING - a python set of words, that should be in the text;
* without - SET of STRING - a python set of words, that shouldn't be in the text;
* at_least - INT - an integer indicating, how many unique words from of the keywords set should at least be in the text. If the number of words is smaller, function returns False;
* at_most - INT - an integer indicating, how many of the keywords should at most be in the text. If the number is bigger, function returns False;
* threshold - FLOAT - threshold for similarity. The smaller the more words the algorithm accepts as similar.
* similarity - textdistance algorithm or embedding_cosine - similarity algorithm. It can be from the textdistance package (e.g. textdistance.hamming.similarity) or embedding_cosine similarity. It can also be a string, one of: "hamming", "embedding_cosine", "levenshtein".

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
