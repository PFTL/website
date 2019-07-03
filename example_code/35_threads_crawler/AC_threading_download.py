from queue import Empty, Queue
from threading import Event, Thread
from time import sleep
from urllib import request
from bs4 import BeautifulSoup


def download_page(queue_downloads, queue_pages, event):
    i = 0
    while not event.is_set():
        try:
            url = queue_downloads.get(timeout=0.5)
        except Empty:
            continue
        if url is None:
            break

        print(f'Getting pages for {url}')
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; PFTLBot/1.0)'}
        req = request.Request('https://en.wikipedia.org'+url, headers=headers)
        response = request.urlopen(req)
        data = response.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        body = soup.find('div', id='bodyContent')
        links = []
        for alink in body.find_all('a'):
            link = alink.get('href')
            if link and link.startswith('/wiki'):
                if not any(x in link for x in ('Category:', 'File:', 'Help:', 'Special:')):
                    links.append(link)
        queue_pages.put({url: links})
        i += 1
    print(f'Downloaded {i} pages in total')


max_depth = 2
queue_down = Queue()
queue_pages = Queue()
event = Event()
depth = 0
initial_page = '/wiki/Shergar'
queue_down.put(initial_page)
pages = {initial_page:
             {'depth': depth,
              'links': None}
              }

threads = []
for i in range(10):
    threads.append(Thread(target=download_page, args=(queue_down, queue_pages, event)))
    threads[-1].start()

while True:
    try:
        new_pages = queue_pages.get(timeout=0.5)
    except Empty:
        continue
    except KeyboardInterrupt:
        event.set()
        break

    page, links = list(new_pages.items())[0]
    print(f'Got {len(links)} links for {page}')
    pages[page]['links'] = links
    if pages[page]['depth'] < max_depth:
        new_depth = pages[page]['depth'] + 1
        for link in links:
            if link not in pages:
                queue_down.put(link)
                pages[link] = {'depth': new_depth,
                               'links': None}
    else:
        print(f'Max depth reached for {page}')
        break

for i in range(10):
    queue_down.put(None)

for t in threads:
    while t.is_alive():
        sleep(0.1)

print('All threads done')
print('Links:')
i = 0
for k in pages:
    print(f'i: {k}')
    i += 1