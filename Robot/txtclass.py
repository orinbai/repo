# -*- coding: utf8 -*-
import jieba, re

chRE = re.compile(u"[\u4e00-\u9fa5, a-z, 0-9]")

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

a = '摩卡世界是一家专业的手机联网游戏开发公司，成立于2 0 0 7年'
print ' '.join(chRE.findall(a.decode('utf8'))).encode('utf8')
exit()
f = open('result/intro.txt')
for lines in f:
    line = lines.decode('utf8').strip().split('\t')
    if line[1] != 'False':
        print line[1].encode('utf8')
        line[1] = F2H(line[1])
        print '/ '.join(jieba.cut(line[1], cut_all=False)).encode('utf8')
        print '---'*30 

f.close()
