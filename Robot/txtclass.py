# -*- coding: utf8 -*-
import jieba, re

MAXLEN = 5
IGSIGN = {',':1, '.':1, '-':1, ';':1, '?':1, ':':1, '"':1, '（':1, '）':1}
#chRE = re.compile(u"[\u4e00-\u9fa5, a-z, 0-9]")
### For NewWord, So Eliminate English Char ###
chRE = re.compile(u"[\u4e00-\u9fa5]")

totalStr = ''
uniqCHAR = {}

def F2H(cstring):
    tstring = ''
    for uchar in cstring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):
            inside_code -= 65248
        tstring += unichr(inside_code)
    return tstring

##### inEfficiency Using Recursion #####
#def enumerateWD(tCopus, sChar, sSign=0):
#    tmparr = []
#    sSign = int(sSign)
#    if tCopus.find(sChar, sSign+1) < 0:
#        return [-1]
#    else:
#        m = tCopus.find(sChar, sSign+1)
#        tmparr.extend([m])
#        tmparr.extend(enumerateWD(tCopus, sChar, m))
#        return tmparr
#########################################

def enumerateWD(tCopus, sChar):
    tmparr = []
    bgSign = 0
    edSign = len(tCopus)
    m = tCopus.find(sChar, 0)
    while m >= 0 :
        yield m
        #tmparr.append(m)
        m = tCopus.find(sChar, m+1)

    

#print enumerateWD(a, '家')
#print a[104:107]
#exit()

f = open('result/intro.txt')
for lines in f:
    line = lines.decode('utf8').strip().split('\t')
    line[1] = line[1].strip()
    if line[1] != 'False' or line[1]:
        m = filter(lambda x: not IGSIGN.has_key(x), chRE.findall(line[1]))
        #print '\n'.join(m).encode('utf8').strip()
        totalStr += ''.join(m).strip()
        for wd in m:
            if uniqCHAR.has_key(wd): continue
            uniqCHAR[wd] = 1
        ########### Check Punctuation ##############
        #print chRE.sub('', line[1]).encode('utf8')#
        ############################################
    else:
        continue
f.close()

for sKey in sorted(uniqCHAR.keys()):
    if not sKey.strip(): continue
    tmparr = []
    print sKey.encode('utf8')
    for i in enumerateWD(totalStr, sKey):
        #tmparr.append(totalStr[i-1:i+5].encode('utf8'))
        tmparr.append(totalStr[i-1:i+5])

    print tmparr[0][0:2].encode('utf8')
    print '--'*10
    print '\n'.join(sorted(tmparr, key=lambda x: x[1:])).encode('utf8')

#print len(totalStr)
#print totalStr[641112:641112+5].encode('utf8')
#print enumerateWD(totalStr, '公'.decode('utf8'))

#print totalStr.encode('utf8')
#print ' '.join(uniqWd.keys()).encode('utf8'), len(uniqWd.keys())
#f = open('result/intro.txt')
#for lines in f:
#    line = lines.decode('utf8').strip().split('\t')
#    if line[1] != 'False':
#        print line[1].encode('utf8')
#        line[1] = F2H(line[1])
#        print '/ '.join(jieba.cut(line[1], cut_all=False)).encode('utf8')
#        print '---'*30 
#
#f.close()
