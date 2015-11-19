from bs4 import BeautifulSoup
f = open('aa.html')
html = f.read()
f.close()
soup = BeautifulSoup(html)

mm = soup.find_all('div', class_='box-content')[0]
for line in soup.find_all('div', class_='box-content'):
    if line.find_all('p'):

    
