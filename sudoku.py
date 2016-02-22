#!/usr/bin/python3
#
# Reference: http://norvig.com/sudoku.html

#   A1 A2 A3 | A4 A5 A6 | A7 A8 A9
#   B1 B2 B3 | B4 B5 B6 | B7 B8 B9
#   C1 C2 C3 | C4 C5 C6 | C7 C8 C9
#   ---------+----------+---------
#   D1 D2 D3 | D4 D5 D6 | D7 D8 D9
#   E1 E2 E3 | E4 E5 E6 | E7 E8 E9
#   F1 F2 F3 | F4 F5 F6 | F7 F8 F9
#   ---------+----------+---------
#   G1 G2 G3 | G4 G5 G6 | G7 G8 G9
#   H1 H2 H3 | H4 H5 H6 | H7 H8 H9
#   I1 I2 I3 | I4 I5 I6 | I7 I8 I9

# grid: a list of 81 squares
# unit: a collection of nine squares (row, column, or box)
# peers: the squares that share a unit

# A puzzle is solved if the squares in each unit are filled with a
# permutation of the digits 1 to 9.

grid1 = '''
    4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
    '''
grid2 = '''
    4 . . |. . . | 8 . 5
    . 3 . |. . . | . . .
    . . . |7 . . | . . .
    ------+------+-------
    . 2 . |. . . | . 6 .
    . . . |. 8 . | 4 . .
    . . . |. 1 . | . . .
    ------+------+-------
    . . . |6 . 3 | . 7 .
    5 . . |2 . . | . . .
    1 . 4 |. . . | . . .
    '''


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

digits = '123456789'
empty = '.0'
alphabet = digits + empty
rows = 'ABCDEFGHI'
cols = '123456789'
squares = cross(rows, cols)     # [A1, A2, A3, ..., I7, I8, I9 ]

# unitlist is a list of lists.
# unitlist: There are 27 units (9 rows, 9 cols, 9 boxes) each with 9 squares.
unitlist = (
    [cross(rows, c) for c in cols] +
    [cross(r, cols) for r in rows] +
    [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
        for cs in ('123', '456', '789')])

# units is a dictionary where each square s maps to the list of units
# that contain the square
# Each square is mapped to 3 units (row, column, box)
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)

# peers is a dictionary where each square s maps to the set of squares
# formed by the union of the squares in the units of s, but not s itself.
# Each square has 20 peers.
peers = dict((s, set(sum(units[s], []))-set([s]))
             for s in squares)


# values: dict of {square: char} where char equals digit or empty ('0' or '.')
def display(values):
    '''
    Display these values as a 2-D grid.
    '''
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) +
              ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)


def grid_values(grid):
    '''
    Convert grid into a dict of {square: char} with '0' or '.' for empties.
    '''
    # filter out all chars in grid that are not in the alphabet
    # (e.g. ' ', '|', '+', '-', '\n')
    chars = [c for c in grid if c in alphabet]
    assert len(chars) == 81
    return dict(zip(squares, chars))


def parse_grid(grid):
    '''
    Convert grid to a dict of possible values, {square: digits},
    or return False if a contradiction is detected.
    '''
    # To start, every square can be any digit;
    # then assign values from the grid.
    values = dict((s, digits) for s in squares)

    for s, d in grid_values(grid).items():
        if d not in digits:
            continue
        if not assign(values, s, d):
            return False
    return values


# values: dict of {square: char} where char equals digit or empty ('0' or '.')
# def assign(values, s, d):
#    '''
#    Eliminate all the other values (except d) from values[s] and propagate.
#    Return values, except return False if a contradiction is detected.
#    '''
#    values[s] = d
#
#    for s in peers[s]:
#        values[s] = values[s].replace(d, '')
#
#    return values


def assign(values, s, d):
    '''
    Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected.
    '''
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    '''
    Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected.
    '''
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')

    # (1) If a square s is reduced to one value d2,
    # then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    # (2) If a unit u is reduced to only one place for a value d,
    # then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def solve(grid):
    return search(parse_grid(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False        # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values       # Solved!
    # Choose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e:
            return e
    return False


def test():
    '''
    A set of unit tests.
    '''
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [
        ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
        ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
        ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(
        ['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
         'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
         'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')


def main():
    test()
    display(parse_grid(grid2))
    display(solve(grid2))


if __name__ == "__main__":
    # execute only if run as a script
    main()
