def bubble_sort(ls):
    if len(ls) == 0 or len(ls) == 1:
        return ls
    else:
        for i in range(len(ls) - 1):
            max_index = 0
            for j in range(0, len(ls) - i - 1):
                if ls[j] > ls[j + 1]:
                    ls[j], ls[j + 1] = ls[j + 1], ls[j]
                    max_index = j
                else:
                    max_index = j
        return ls

