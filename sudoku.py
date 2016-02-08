#!/usr/bin/python3

grid1 = '123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789'
grid2 = """
	. . . |. . . | . . . 
	. . . |. . . | . . . 
	. . . |. . . | . . .
	------+------+------- 
	. . . |. . . | . . . 
	. . . |. . . | . . . 
	. . . |. . . | . . . 
	------+------+------- 
	. . . |. . . | . . . 
	. . . |. . . | . . . 
	. . . |. . . | . . . 
	"""
grid3 = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
	
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]
    
digits	= '123456789'
empty	= '.0'
alphabet = digits + empty
rows	= 'ABCDEFGHI'
cols	= '123456789'
squares = cross(rows, cols)

unitlist = ([cross(rows, c) for c in cols]
	+ [cross(r, cols) for r in rows]
	+ [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
	
# units is a dictionary where each square maps to the list of units that contain the square
units = dict((s, [u for u in unitlist if s in u]) 
             for s in squares)

# peers is a dictionary where each square s maps to the set of squares formed by the 
# union of the squares in the units of s, but not s itself 
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)
    
def display(values):
	"Display these values as a 2-D grid."
	width = 11 # 1 + max(len(values[s]) for s in squares)
	line = '+'.join(['-' * (width * 3)] * 3)
	for r in rows:
		print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
			for c in cols))
		if r in 'CF':
			print(line)
                         
def grid_values(grid):
	"Convert grid into a dict of {square: char} with '0' or '.' for empties."
	chars = [c for c in grid if c in alphabet]
	assert len(chars) == 81
	return dict(zip(squares, chars))

def parse_grid(grid):
	"""Convert grid to a dict of possible values, {square: digits},
	or return False if a contradiction is detected."""	
    ## To start, every square can be any digit; then assign values from the grid.
	values = dict((s, digits) for s in squares)
	
	for s, d in grid_values(grid).items():
		if not d in digits:
			continue
		if not assign(values, s, d):
			return False		
	return values

def assign(values, s, d):
	"""Eliminate all the other values (except d) from values[s] and propagate.
	Return values, except return False if a contradiction is detected."""
	values[s] = d
	
	for s in peers[s]:
		values[s] = values[s].replace(d, '')
		
	for u in units[s]:
		dplaces = [s for s in u if d in values[s]]
		
	return values			
	
	
def test():
    "A set of unit tests."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')

def main():
	test()
	display(parse_grid(grid3))
		
if __name__ == "__main__":
    # execute only if run as a script
    main() 
	