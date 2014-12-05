# DiMint_Client

## Installation
```
pip install -e git+git://github.com/DiMint/DiMint_Client@master#egg=dimint_client.egg
```
## How to use
```python
from dimint_client import DiMintClient

dimint = DiMintdimint('127.0.0.1', 5556)

# Get overlord host list
print(dimint.get_overlord_list())

# Get Value from DiMint Server
value1 = dimint.get('key1') # dimint['key1'] also work

# Set Value to DiMint Server
dimint.set('key2', [1,2,3,4,5]) # dimint['key2'] = [1,2,3,4,5] also work

# Get states of all nodes
states = dimint.get_state()

```
