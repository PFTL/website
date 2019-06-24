import os
from time import time
from urllib import request


website_list = [
    'https://www.wikipedia.org/',
    'https://nl.wikipedia.org/',
    'https://de.wikipedia.org/',
    'https://fr.wikipedia.org/',
    'https://pt.wikipedia.org/',
    'https://it.wikipedia.org',
    'https://ru.wikipedia.org',
    'https://es.wikipedia.org',
    'https://en.wikipedia.org',
    'https://ja.wikipedia.org',
    'https://zh.wikipedia.org',
]

def download_data(website):
    response = request.urlopen(website)
    data = response.read()
    save_data(data)

def save_data(data):
    i = 0
    while os.path.exists(f'website_data_{i}.dat'):
        i += 1
    with open(f'website_data_{i}.dat', 'wb') as f:
        f.write(data)

t0 = time()
for ws in website_list:
    download_data(ws)

print(f'Downloading {len(website_list)} websites took {time()-t0:2.2f} seconds')