from dimint_client import DiMintClient

client = DiMintClient('127.0.0.1', 5556)

print(client.set('key1', 'asdf'))
print(client['key1'])
