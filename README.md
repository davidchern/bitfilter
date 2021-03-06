# bitfilter

An implementation analogous to bloom filter, for efficiently storing, retrieving and deleting/erasing positive integer numbers, also scalable to data size.

Typically, it can be used for keeping records of user ids that are associated to an item (e.g. a file marked by some users).

### Requirement

No any third-party libraries, except for python buildin libraries.

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

# store another number 321 to the bit
bit.set(321)
321 in bit # -> True

# delete/erase a number from the bit
bit.delete(123)
bit.get(123) # -> 0

# get the compressed binary data from the bit
data = bit.tobytes()
with open('bit.dat', 'wb') as fd:
    fd.write(data)

# load the compressed binary data into the bit
with open('bit.dat', 'rb') as fd:
    data = fd.read()
    bit2 = BitFilter(data=data)
```

The compressed binary data can also be stored with `models.BinaryField` in Django.

```python
from django.db import models
from bitfilter import BitFilter


class File(models.Model):

    markers = models.BinaryField(default=None, max_length=1024)
    likers = models.BinaryField(default=None, max_length=1024)
     
    def set_record(self, name, uid):
        bit = BitFilter(data=getattr(self, name))
        bit.set(uid)
        setattr(self, name, bit.tobytes())
        self.save(update_fields=[name])

    def del_record(self, name, uid):
        bit = BitFilter(data=getattr(self, name))
        bit.delete(uid)
        setattr(self, name, bit.tobytes())
        self.save(update_fields=[name])

    def has_record(self, name, uid):
        return BitFilter(data=getattr(self, name)).get(uid)
        
```

Hope you'll like it.
