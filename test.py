from dimint_client import DiMintClient

c1 = DiMintClient('127.0.0.1', 5556)
c2 = DiMintClient('127.0.0.1', 5556)

print(c1.set('key1', 'asdf'))
print(c2.set('key2', 'fsdfsd'))
print(c1['key1'])
print(c2['key2'])
