from bs4 import BeautifulSoup
from urllib import request


def get_pages(url, level=0, max_depth=1):
    print(f'{level} Getting pages for {url}')
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PFTLBot/1.0)'}
    req = request.Request('https://en.wikipedia.org'+url, headers=headers)
    response = request.urlopen(req)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    body = soup.find('div', id='bodyContent')
    pages = []
    for alink in body.find_all('a'):
        link = alink.get('href')
        if link and link.startswith('/wiki'):
            if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
                pages.append(link)
                if level < max_depth:
                    pages += get_pages(link, level=level+1)
    return pages


url = '/wiki/Shergar'
pages = get_pages(url)
print(len(pages))