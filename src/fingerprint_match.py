def match(pattern, text):
    if len(pattern) > len(text) or len(pattern[0]) > len(text[0]):
        return None
    fingerprint = get_fingerprint(pattern, pattern)
    for i in range(len(text)-len(pattern)+1):
        region_fingerprint = get_fingerprint(text, pattern, i)
        for j in range(len(text[0])-len(pattern[0])+1):
            prev_col = 0
            next_col = 0
            if j >0:
                for c in range(len(pattern)):
                    prev_col = prev_col ^ text[i+c][j-1]
                    next_col = next_col ^ text[i+c][j+len(pattern[0])-1]
            region_fingerprint = region_fingerprint ^ next_col ^ prev_col
            if fingerprint == region_fingerprint:
                if check_match(pattern, text, i, j):
                    return (i,j)
    return None

def get_fingerprint(text, pattern, r=0, c=0):
    fingerprint = 0
    for i in range(0, len(pattern)):
        for j in range(len(pattern[0])):
            fingerprint = fingerprint ^ text[i+r][j+c]
    return fingerprint

def check_match(pattern, text, r, c):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if pattern[i][j] != text[i+r][j+c]:
                return False
    return True