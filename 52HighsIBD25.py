import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://ycharts.com/companies/FFTY/holdings"
req = Request(url, headers={'User-Agent': 'Safari/8536.25'})
html = urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

#MAKE LIST OF STOCK SYMBOLS
symbolList = list()
tags =  soup('a')
for tag in tags:
    possibleSymbol = tag.get('href', None)
    if possibleSymbol is None:
        continue
    elif possibleSymbol.find('/companies/') >=0 and tag.string.find(possibleSymbol[11:len(possibleSymbol)]) != -1:
        symbolList.append(possibleSymbol[11:len(possibleSymbol)])
# print(symbolList)

#MAKE LIST OF STOCK NAMES
nameList = list()
nameTags = soup('td')
for tag in nameTags:
    possibleSymbol = tag.get('class', None)
    if possibleSymbol is None:
        print("none")
        continue
    elif possibleSymbol.count("col2") > 0 and not tag.string.isdigit():
        nameList.append(tag.string)
# print(nameList)

#FIND STOCKS HITTING 52 WEEK HIGHS
url = "https://www.marketbeat.com/market-data/52-week-highs/"
req = Request(url, headers={'User-Agent': 'Safari/8536.25'})
html = urlopen(req, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

highList = list()
tags =  soup('a')
for tag in tags:
    possibleSymbol = tag.get('href', None)
    if possibleSymbol is None:
        continue
    elif possibleSymbol.find('/stocks/') >=0 and len(tag.string) < 5:
        highList.append(tag.string)
# print(highList)

#FIND MATCHES BETWEEN IBD25 AND 52 WEEK HIGHS
print(set(symbolList).intersection(highList))
