def nqueens(n):
    queens = []
    return search(n, queens)

def horizontal_check(current, queens):
    if current in queens:
        return False
    else:
        return True

def diagonal_check(current, queens):
    row = len(queens)
    for other_row in range(row):
        col = queens[other_row]
        if abs(current - col) == abs(row - other_row):
            return False
    return True

def search(n, queens):
    if len(queens) == n:
        return queens
    for current in range(n):
        if horizontal_check(current, queens) and diagonal_check(current, queens):
            new_queens = queens + [current]
            potential = search(n, new_queens)
            if potential:
                return potential
    return False
