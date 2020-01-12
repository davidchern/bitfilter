# bitfilter

An implementation analogous to bloom filter, for efficiently storing and deleting number in it, also scalable to data size.

### Usage

```python
from bitfilter import BitFilter

bit = BitFilter(size=1000)
# store a number 123 to the bit
bit.set(123)
# get if a number has been stored into the bit.
bit.get(123) # -> 1
bit.get(321) # -> 0
123 in bit # -> True
321 in bit # -> False
# delete/erase a number from the bit
bit.delete(123)
bit.get(123) # -> 0
# get the compressed binary data from the bit
data = bit.tobytes()
# load the compressed binary data into the bit
bit2 = BitFilter(data=data)
```
