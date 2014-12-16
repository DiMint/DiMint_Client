from dimint_client import DiMintClient

c = DiMintClient('127.0.0.1', '5556')

print("Set")
for i in range(1, 5000):
    v = c.set('key_{0}'.format(i), i * i)
    print('storage[key_{0}] = {1}'.format(i, v))

print("Get")
for i in range(1, 5000):
    print('storage[key_{0}] = {1}'.format(i, c['key_{0}'.format(i)]))

print("Strong Get")
for i in range(1, 5000):
    print('storage.get_strong(key_{0}) = {1}'.format(
        i, c.get_strong('key_{0}'.format(i))))
