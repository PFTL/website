from urllib.request import Request

from bs4 import BeautifulSoup
from urllib import request


headers = {'User-Agent': 'Mozilla/5.0 (compatible; PFTLBot/1.0)'}
req = request.Request('https://en.wikipedia.org/wiki/Shergar', headers=headers)
response = request.urlopen(req)
data = response.read().decode('utf-8')

soup = BeautifulSoup(data, 'html.parser')
# print(soup.prettify())
body = soup.find('div', id='bodyContent')
# for link in body.find_all('a'):
#     print(link.get('href'))

links = []
for alink in body.find_all('a'):
    link = alink.get('href')
    if link and link.startswith('/wiki'):
        if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
            print(link)
            links.append(link)

print(len(links))