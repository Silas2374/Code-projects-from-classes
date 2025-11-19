import math

class BloomFilter:
    def __init__(self):
        self.filter_ = 0
    def add(self, key):
        hash_code = abs(hash(key)) % pow(2,32) # get hash code and make it less than 2^32
        hash1 = hash_code >> 16 # 16 higher order bits
        hash2 = hash_code & 2**16-1 # 16 lower order bits
        # set filter_  by shifting 1 left hash1 number of bits
        self.filter_ = self.filter_ | 1 << hash1
        self.filter_ = self.filter_ | 1 << hash2
    def might_contain(self, key):
        hash_code = abs(hash(key)) % pow(2, 32)
        hash1 = hash_code >> 16
        hash2 = hash_code & 2 ** 16 - 1
        # checking the bit by shifting right hash1 number of bits and checking the last bit
        if self.filter_ >> hash1 & 1 and self.filter_ >> hash2 & 1:
            return True
        return False

    def _true_bits(self):
        return self._true_bits_recursion(self.filter_)

    def _true_bits_recursion(self, bits):
        if bits == 0:
            return 0
        if bits == 1:
            return 1
        length = int(math.log(bits, 2)) + 1
        return self._true_bits_recursion(bits >> length // 2) + self._true_bits_recursion(
            bits & 2 ** (length // 2) - 1)
