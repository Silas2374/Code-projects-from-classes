#Simple 2D pattern matching algorithm

def match(pattern, text):
    m = len(pattern)
    n = len(text)
    if m == 0 or n == 0 or m > n:
        return None
    for row in range(n - m + 1):
        for col in range(n - m + 1):
            found_match = True
            for i in range(m):
                for j in range(m):
                    if text[row + i][col + j] != pattern[i][j]:
                        found_match = False
                        break
            if found_match:
                return row, col
    return None