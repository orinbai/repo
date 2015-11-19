#coding=utf8
from bs4 import BeautifulSoup
import re, time, os

baseurl = 'http://zdb.pedaily.cn/inv/'
strip_capital = re.compile('(,\/,| \/,)')

def tdParse(soupobj):
    ### Total 6 td, So Do With a For Loop ###
    tmpArray = []

    for i in range(1,7):
        b = soupobj.find('td', class_='td%d' % i)
        if b is not None:
            if b.a is not None:
                ttmpArray = []
                for achild in b.find_all('a'):
                    if achild.string:
                        ttmpArray.append(achild.string)
                    else:
                        ttmpArray.append('-')
                else:
                    tmpArray.append('|'.join(ttmpArray))
            else:
                tmpArray.append(b.string)
        else:
            return False

    return tmpArray


def parseHTML(tmphtml):
    ### Extract Infomation ###
    toArray = []
    soup = BeautifulSoup(tmphtml)

    startSIGN = soup.find('table',class_='zdb-table zdb-inv-table')
    for child in startSIGN.children:
        if child.find('td') < 0: continue
        toArray.append(tdParse(child))
    return toArray

def downPage(pageNum):
    import urllib2
    baseurl = 'http://zdb.pedaily.cn/inv/'
    if (pageNum < 1):
        url = baseurl
    else:
        url = '%s%s' % (baseurl, str(pageNum))

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'  
    req = urllib2.Request(url)
    req.add_header('User-Agent', user_agent)
    try:
        response = urllib2.urlopen(req, timeout=5)
        return response.read()
    except:
        return False

def wriLog(filename, content):
    baseDir = '/home/orin/Learning/Robot'
    if filename=='err_log':
        f = open('%s/err_log' % baseDir, 'a')
    else:
        f = open('%s/tmpfile/%s' % (baseDir, filename), 'w')

    f.write(content)
    f.close()



#html = downPage(0)
#if html:
#    wriLog('index.html', html)
#else:
#    print 'Init Failed'
#    exit()
### Get Total Page Num ##
#soup = BeautifulSoup(html)
#MAXPAGE = int([x for x in soup.find('div', class_='page-list page').stripped_strings][5])
#
#for i in range(1, MAXPAGE+1):
#    print 'Now Downloading Page %d' % i
#    html = downPage(i)
#    if html:
#        wriLog('%d.html' % i, html)
#    else:
#        wriLog('err_log', 'Mistake when download Page %d\n' % i)
#
#    time.sleep(30)

## Download Again ##
#f = open('err_log.2')
#for line in f:
#    tmpa = int(line.strip().split()[4])
#    print 'Download Page %d' % tmpa
#    html = downPage(tmpa)
#    if html:
#        wriLog('%d.html' % tmpa, html)
#    else:
#        wriLog('err_log', 'Mistake when download Page %d, again\n' % tmpa)
#
#    time.sleep(30)
#
#
#f.close()


## Parse HTML to Array ##

fileList = os.listdir('tmpfile')
allrecord = []
for singlefile in sorted(fileList, key=lambda x: int(x.split('.')[0])):
    f = open('tmpfile/%s' % singlefile)
    html = f.read().decode('utf8')
    f.close()
    allrecord.extend(parseHTML(html))

for ele in allrecord:
    print '\t'.join(ele).encode('utf8')
