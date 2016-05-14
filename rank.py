import sys
from urlparse import urlparse

penalty_ext = ['ga','tk','ml','cf','free']
good_ext = ['com', 'net', 'org']
important_ext = ['gov','mil','edu']

rank = 1000
url = sys.argv[1]
title = sys.argv[2]
nol = sys.argv[3]

url_p = urlparse(url)

url_ext = url_p.netloc.split('.')[-2:]
url_ext = url_ext[1]
url_scheme = url_p.scheme


if title == '' or title == 'Untitled' or title == 'untitled':
    rank = rank * 0.8

while 1==1:
    if url_ext in penalty_ext:
        rank = rank * 0.9
        break
    if url_ext in good_ext:
        rank = rank * 1.1
        break
    if url_ext in important_ext:
        rank = rank * 1.2
        break
    break
if len(url) <= 25:
    rank = rank + 50
elif len(url) <= 30:
    rank = rank + 25
elif len(url) >= 60:
    rank = rank - 25

if len(title) <= 10:
    rank = rank + 25
elif len(title) >= 69:
    rank = rank - 30

if nol > 0 and nol <= 5:
    rank = rank + 20
elif nol > 50:
    rank = rank - 50

if url_scheme == 'https':
    rank = rank + 50
elif url_scheme == 'http':
    rank = rank + 5
else:
    rank = rank * 0

rank = str(rank)
if '.' in rank:
    rank = rank.split('.')
    rank = rank[0]
print rank