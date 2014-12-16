from dimint_client import DiMintClient
import time

c = DiMintClient('127.0.0.1', '5556')

print("Set")
for i in range(1, 5000):
    v = c.set('key_{0}'.format(i), i * i)
    print('storage[key_{0}] = {1}'.format(i, v))

print("Get")
for i in range(1, 5000):
    print('storage[key_{0}] = {1}'.format(i, c['key_{0}'.format(i)]))
