from asyncio import sleep as async_sleep
from time import sleep as time_sleep

print('1')
async_sleep(1)
print('2')
time_sleep(1)
print('3')