import os
import base64
import urllib2
import subprocess
import urlparse
import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup

os.system('cls')
url_list = ['https://en.wikipedia.org/wiki/Islamic_State_of_Iraq_and_the_Levant']

print '-----------------------'
print ' Claw Search 0.5 beta'
print '-----------------------'

future_url = []
print '[START] Crawling %s...' % (url_list[0])

try:
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Claw Search Bot 0.5 beta')]
    response = opener.open(url_list[0])
except:
    print '[ERROR] Invalid starter URL. Terminating...'
    os.system('killall python')
url_final = response.geturl()
if url_final is not url_list[0]:
    url_list.append(url_list[0])
    print '>> [INFO] Redirect to (%s)' % (url_final)

url_html = response.read()
soup = BeautifulSoup(url_html, "html.parser")

# URL info
url_final = base64.b64encode(url_final)
url_title = base64.b64encode(soup.title.string)
#url_text = base64.b64encode(nltk.clean_html(url_html))

#CLEAN HTML
for script in soup(["script", "style"]):
    script.extract()
url_text = soup.get_text()
lines = (line.strip() for line in url_text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
url_text = '\n'.join(chunk for chunk in chunks if chunk)
##url_text = base64.b64encode(re.sub(r'(\r\n.?)+', r'\r\n', url_text))

safe_title = soup.title.string
if '"' in safe_title:
    safe_title = safe_title.relplace('"', "'")

# Get links
print '>> [INFO] Extracting links...'
n=0
for link in soup.find_all('a'):
    try:
        l = link.get('href')
        if '#' in l:
            l = l.split('#')
            l = l[0]

        if l[:10] == 'javascript':
            continue

        if l[:4] == 'http':
            future_url.append(l)
            n=n+1
            continue
        else:
            l = urlparse.urljoin(base64.b64decode(url_final), l)

        if l[:4] == 'http':
            future_url.append(l)
            with open("future.txt", "a") as myfile:
                myfile.write(l+"\n")
            n=n+1
            continue
    except:
        continue
nol = str(n)
rank = '0'#subprocess.check_output("python rank.py "+base64.b64decode(url_final)+" \""+base64.b64decode(url_title)+"\" "+nol, shell=True)
print '>> [INFO] Rank is %s.' % (rank)
print '>> [INFO] Adding URL to the database.'
print 'Rank: ' + rank
try:
    addDB = subprocess.check_output("php add.php '" + url_final + "' '" + url_title + "' '" + url_text + "' "+ rank, shell=True)
except:
    print '>> [WARNING] Page is too large. Using alternative method of adding.'
    f = open('./temp/'+url_final[:5]+'.txt', 'w')
    f.write(url_text)
    f.close()
    addDB = subprocess.check_output("php add_alt.php '" + url_final + "' '" + url_title + "' '" + './temp/'+url_final[:5]+'.txt' + "' "+rank, shell=True)

if addDB == '1':
    print '>>> [SUCCESS] URL has been added.', addDB
else:
    print '>>> [ERROR] URL was not added.', addDB
print '---------------'
print ''
url_list.append(base64.b64decode(url_final))


while len(future_url) > 0:
    print '---------------'
    if future_url[0] in url_list:
        future_url.pop(0)
        print '[ERROR] URL is already in the database.'
        print '---------------'
        print ''
        print ''
        continue
    check = subprocess.check_output("php action.php check '" + future_url[0] + "'", shell=True)
    if check == 'in':
        print '[ERROR] URL is already in the database. (from PHP: %s)' % (check)
        print '---------------'
        print ''
        print ''
        continue
    print '[CRAWLER] Crawling %s...' % (future_url[0])
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Claw Search Bot 0.5 beta http://claw.ga/')]
        response = opener.open(future_url[0])
    except:
        print '[ERROR] Invalid URL.'
        continue
    url_final = response.geturl()

    if url_final is not future_url[0]:
        url_list.append(future_url[0])
        print '>> [INFO] There is a redirect to (%s)' % (url_final)
    else:
        url_list.append(future_url)

    url_html = response.read()
    soup = BeautifulSoup(url_html, "html.parser")

    # URL info
    url_final = base64.b64encode(url_final)
    try:
        url_title = base64.b64encode(soup.title.string)
    except:
        url_title = base64.b64encode('Untitled')
    if base64.b64decode(url_title) == '':
        url_title = base64.b64encode('Untitled')
    safe_title = base64.b64decode(url_title)
    if '"' in safe_title:
        safe_title = safe_title.relplace('"', "'")
    print '>> [INFO] Cleaning HTML.'
    #url_text = base64.b64encode(nltk.clean_html(url_html))

	#CLEAN HTML
    for script in soup(["script", "style"]):
        script.extract()
    url_text = soup.get_text()
    lines = (line.strip() for line in url_text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    url_text = '\n'.join(chunk for chunk in chunks if chunk)
    url_text = base64.b64encode(url_text)

	#Get links
    print '>> [INFO] Extracting links...'
    n=0
    for link in soup.find_all('a'):
        try:
            l = link.get('href')
            if l in url_list:
                continue
            if l in future_url:
                continue
            if '#' in l:
                l = l.split('#')
                l = l[0]
                if l in url_list:
                    continue
                if l in future_url:
                    continue

            if l[:10] == 'javascript':
                continue

            if l[:4] == 'http':
                if l in url_list:
                    continue
                if l in future_url:
                    continue
                future_url.append(l)
                n=n+1
                continue
            else:
                l = urlparse.urljoin(base64.b64decode(url_final), l)

            if l[:4] == 'http':
                if l in url_list:
                    continue
                if l in future_url:
                    continue
                future_url.append(l)
                n=n+1
                with open("future.txt", "a") as myfile:
                    myfile.write(l+"\n")
                continue
        except:
            continue
    nol = str(n)
    rank = '0'#subprocess.check_output("python rank.py "+base64.b64decode(url_final)+" \""+base64.b64decode(url_title)+"\" "+nol, shell=True)
    print '>> [INFO] Rank is %s.' % (rank)
    print '>> [INFO] Adding URL to the database.'
    try:
        addDB = subprocess.check_output("php add.php '" + url_final + "' '" + url_title + "' '" + url_text + "' "+rank, shell=True)
    except:
        print '>> [WARNING] Page is too large. Using alternative method of adding.'
        f = open('./temp/'+url_final[:5]+'.txt', 'w')
        f.write(url_text)
        f.close()
        addDB = subprocess.check_output("php add_alt.php '" + url_final + "' '" + url_title + "' '" + './temp/'+url_final[:5]+'.txt' + "' "+rank, shell=True)

    if addDB == '1':
        print '>>> [SUCCESS] URL has been added.'
    else:
        print '>>> [ERROR] URL was not added. (Response: %s)' % (addDB)
    print '---------------'
    print ''
    print ''
    future_url.pop(0)
print "Script finished."
