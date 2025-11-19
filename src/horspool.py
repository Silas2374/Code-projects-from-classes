class HorspoolStringMatcher:
    def __init__(self, pattern):
        self.pattern = pattern
        self.shift_table = self.create_table()
        self.default_shift = len(pattern)

    def match(self, text):
        pattern_len = len(self.pattern)
        text_len = len(text)
        if pattern_len > text_len:
            return -1
        i = pattern_len - 1
        while i < text_len:
            k = 0
            while k < pattern_len and self.pattern[pattern_len - 1 - k] == text[i - k]:
                k += 1
            if k == pattern_len:
                return i - pattern_len + 1
            else:
                i += self._get_shift(text[i])
        return -1

    def create_table(self):
        m = len(self.pattern)
        shift_table = {}
        for i in range(m - 1):
            char = self.pattern[i]
            shift_table[char] = m - 1 - i
        return shift_table

    def _get_shift(self, char):
        shift_table = self.shift_table
        return shift_table.get(char, self.default_shift)