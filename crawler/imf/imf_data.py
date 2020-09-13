import requests
import json
from html2json import collect
import html2text
from lxml import html
import requests
import re


url = "https://www.imf.org/en/Topics/imf-and-covid19/Policy-Responses-to-COVID-19"


result = requests.get(url)
#print(result.content)
#tree = html.fromstring(result.content)
m = re.search('(?:\<h3\>)([\w;:\[\{\]\}\\\|\<\>/?, &!@#$%^&**()\-_+=~`.\n\t\r]*)(?:\<h3\>)', result.content.decode("utf-8"))
print(m)

# TODO insert results into database
