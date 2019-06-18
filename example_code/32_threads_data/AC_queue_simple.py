from queue import Queue

queue = Queue()
for i in range(20):
    queue.put(i)

while not queue.empty():
    data = queue.get()
    print(data)