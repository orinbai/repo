a = '123a123a123a123a123a'

def aaaa(x, y=0):
    #y = int(y)
    print y
    if x.find('a', y+1) < 0:
        return str(-1)
    else:
        print "**"*5
        m = x.find('a', y+1)
        #return list(str(m)) + list(aaaa(a, m))
        return str(m) + ',' + aaaa(a, m)

print aaaa(a).split(',')
