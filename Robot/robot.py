#coding=utf8
from bs4 import BeautifulSoup
import re, time, os, random, sys, urllib

SLEEPTIME = 10

baseurl = 'http://zdb.pedaily.cn'
strip_capital = re.compile('(,\/,| \/,)')
fmt_span = re.compile('<span[^>]*>')
fmt_span1 = re.compile('<\/span>')

def extractINFO(soupobj):
    tmpArray = []
    for line in soupobj.find_all('div', class_='box-content'):
        for contents in line.find_all('p'):
            content = ','.join(contents.stripped_strings)
            if '联系电话'.decode('utf8') in content: continue
            if content:
                tmpArray.append(content)
    else:
        ### For Nest Div ###
        if not tmpArray:
            for line in soupobj.find_all('div', id='cke_pastebin'):
                if line.string:
                    tmpArray.append(line.string.strip())
                elif line.parent.attrs.has_key('id') and line.parent.attrs['id'] == 'cke_pastebin':
                        tmpArray.append(line.string.strip())
    return ''.join(tmpArray)

            

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

def downPage(baseURL):
    import urllib2

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'  
    req = urllib2.Request(baseURL)
    req.add_header('User-Agent', user_agent)
    try:
        response = urllib2.urlopen(req, timeout=10)
        return response.read()
    except:
        print sys.exc_info()
        return False

def wriLog(filename, content):
    baseDir = '/home/orin/Learning/Robot'
    if filename=='err_log':
        f = open('%s/err_log' % baseDir, 'a')
    else:
        f = open('%s/tmpfile/%s' % (baseDir, filename), 'w')

    f.write(content)
    f.close()



### Get Total Page Num ##
#soup = BeautifulSoup(html)
#MAXPAGE = int([x for x in soup.find('div', class_='page-list page').stripped_strings][5])
#
#for i in range(1, MAXPAGE+1):
#    print 'Now Downloading Page %d' % i
#    url = '%s/inv/%d' % (baseurl, i)
#    html = downPage(url)
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
#fileList = filter(lambda x: x.endswith('html'), os.listdir('tmpfile'))
#allrecord = []
#for singlefile in sorted(fileList, key=lambda x: int(x.split('.')[0])):
#    f = open('tmpfile/%s' % singlefile)
#    html = f.read().decode('utf8')
#    f.close()
#    allrecord.extend(parseHTML(html))
#
#for ele in allrecord:
#    print '\t'.join(ele).encode('utf8')

## Download Introduction ##
#f = open('conf/SUname.conf')
#filelist = map(lambda x: x.split('.')[0], filter(lambda x: x.endswith('intro'), os.listdir('tmpfile')))
#for line in f:
#    id, name = line.decode('utf8').strip().split('\t')
#    if id in filelist: continue
#    print 'Download Page %s at %s' % (name.encode('utf8'), time.asctime(time.localtime(time.time())))
#    name = urllib.quote(name.encode('utf8'))
#    url = '%s/enterprise/%s/' % (baseurl, name)
#    html = downPage(url)
#    if html:
#        wriLog('%s.intro' % id, html)
#    else:
#        wriLog('err_log', 'Mistake when download Page %s\n' % id)
#
#    time.sleep(SLEEPTIME+random.randint(0,5))
#f.close()


### Extract Introduction of Company ###
allfile = filter(lambda x: x.endswith('intro'), os.listdir('tmpfile'))
f = open('result/intro.txt', 'w')
#allfile = ['2144.intro']
for singlefile in allfile:
    ftmp = open('tmpfile/%s' % singlefile)
    html = ftmp.read().decode('utf8')
    html = fmt_span.sub('', html)
    html = fmt_span1.sub('', html)
    ftmp.close()
    soup = BeautifulSoup(html)
    singleIntro = extractINFO(soup)
    if singleIntro:
        f.write('%s\t%s\n' % (singlefile.split('.')[0], singleIntro.encode('utf8')))
    else:
        print '-'*40
        print singlefile
        f.write('%s\tFalse\n' % (singlefile.split('.')[0]))
f.close()

