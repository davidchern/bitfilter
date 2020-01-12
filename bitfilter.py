# Bitfilter: an implementation analogous to Bloomfilter.
# It is also scalable according to data.
# @Modified by David Chern, 2019/10/19
# @Adopted from:
# https://stackoverflow.com/questions/311202/modern-high-performance-bloom-filter-in-python
# https://stackoverflow.com/questions/47981/how-do-you-set-clear-and-toggle-a-single-bit
import array, zlib


class BitFilter(object):

    def __init__(self, size=10000, data=None):
        if data is None:
            self.bits = array.array('B', [0 for _ in range((size + 7) // 8)])
        else:
            self.frombytes(data)
        self.maxbit = len(self.bits) * 8

    def __len__(self):
        return len(self.bits)

    def __repr__(self):
        return "<BitFilter: maxbit=%i, datalen=%i bytes, typecode='%s'>" % (
                self.maxbit, len(self.bits), self.bits.typecode
            )

    def set(self, bit):
        if bit < self.maxbit:
            self.bits[bit // 8] |= 1 << (bit % 8)
        else:
            index = bit // 8
            self.bits.extend(array.array('B', [
                0 for _ in range(index - len(self.bits) + 1)
            ]))
            self.maxbit = len(self.bits) * 8
            self.bits[index] |= 1 << (bit % 8)

    def delete(self, bit):
        if bit < self.maxbit:
            self.bits[bit // 8] &= ~(1 << (bit % 8))

    def get(self, bit):
        if bit < self.maxbit:
            return (self.bits[bit // 8] >> (bit % 8)) & 1
        return 0

    def __contains__(self, bit):
        if bit < self.maxbit:
            if (self.bits[bit // 8] >> (bit % 8)) & 1:
                return True
        return False

    def data(self):
        # It takes about 1.5-2 us to fetch data for every item of the array.
        # So it should be avoided to fetch all data in a BitFilter with large
        # size. e.g., fetching all data in 125,000,000 items costs 22 seconds.
        return [
            bit
            for bit in range(self.maxbit)
            if (self.bits[bit // 8] >> (bit % 8) & 1)
        ]

    def tobytes(self):
        return zlib.compress(self.bits.tobytes())

    def frombytes(self, data):
        bits = array.array('B')
        bits.frombytes(zlib.decompress(data))
        self.bits = bits

