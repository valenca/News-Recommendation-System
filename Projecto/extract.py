from bs4 import BeautifulSoup
import urllib

url = "http://www.bbc.co.uk/news/world-europe-27065782#sa-ns_mchannel=rss&amp;ns_source=PublicRSS20-sa"
url = "http://www.bbc.com/news/science-environment-26925271"
url = "http://www.bbc.com/news/business-27049101"

html = urllib.urlopen(url).read()

soup = BeautifulSoup(html,'html5lib')
print str(soup.title)[7:-8]
content = [div for div in soup.find_all('div') if str(div)[:24] == '<div class="story-body">']
soup = BeautifulSoup(str(content[0]),'html5lib')
[par.extract() for par in soup.findAll('p') if str(par.findParent())[:24] != '<div class="story-body">']
paragraphs = [par for par in soup.findAll('p')]
soup = BeautifulSoup(' '.join(list(map(str,paragraphs))),'html5lib')
print(soup.get_text())

