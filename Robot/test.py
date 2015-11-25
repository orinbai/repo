# -*- coding: utf8 -*-
from bs4 import BeautifulSoup
f = open('tmpfile/735.intro')
html = f.read().decode('utf8')
f.close()
soup = BeautifulSoup(html)

mm = soup.find_all('div', id='cke_pastebin')
print mm
print '\n'.join(map(lambda x: x.string, mm))
exit()
for line in soup.find_all('div', class_='box-content'):
    print line
    for contents in line.find_all('p'):
        print contents
        if contents.div:
            print 'oooo'
            print contents.div.stripped_strings
        content = ','.join(contents.stripped_strings)
        
        if '联系电话'.decode('utf8') in content: continue
        continue
        if content:
            print content.encode('utf8')
            print '-'*20
