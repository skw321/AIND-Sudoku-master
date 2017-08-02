def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
	
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i] + cols[i] for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


naked_twins_test_1 = {"G7": "1234568", "G6": "9", "G5": "35678", "G4": "23678", "G3": "245678", "G2": "123568", "G1": "1234678", "G9": "12345678", "G8": "1234567", "C9": "13456", "C8": "13456", "C3": "4678", "C2": "68", "C1": "4678", "C7": "13456", "C6": "368", "C5": "2", "A4": "5", "A9": "2346", "A8": "2346", "F1": "123689", "F2": "7", "F3": "25689", "F4": "23468", "F5": "1345689", "F6": "23568", "F7": "1234568", "F8": "1234569", "F9": "1234568", "B4": "46", "B5": "46", "B6": "1", "B7": "7", "E9": "12345678", "B1": "5", "B2": "2", "B3": "3", "C4": "9", "B8": "8", "B9": "9", "I9": "1235678", "I8": "123567", "I1": "123678", "I3": "25678", "I2": "123568", "I5": "35678", "I4": "23678", "I7": "9", "I6": "4", "A1": "2468", "A3": "1", "A2": "9", "A5": "3468", "E8": "12345679", "A7": "2346", "A6": "7", "E5": "13456789", "E4": "234678", "E7": "1234568", "E6": "23568", "E1": "123689", "E3": "25689", "E2": "123568", "H8": "234567", "H9": "2345678", "H2": "23568", "H3": "2456789", "H1": "2346789", "H6": "23568", "H7": "234568", "H4": "1", "H5": "35678", "D8": "1235679", "D9": "1235678", "D6": "23568", "D7": "123568", "D4": "23678", "D5": "1356789", "D2": "4", "D3": "25689", "D1": "123689"}


assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins

#Find all instances of naked twins
    twin_pair_list= []
    for unit in unitlist:
        value_list = [ values[box] for box in unit ] 
        for box in unit:
            if len(values[box]) == 2 and value_list.count(values[box]) == 2 :
                for i in range(unit.index(box)+1,len(unit),1):
                    index = unit[i]
                    if values[box] == values[index]:
                        twin_pair_list.insert(0,(box,index))
    #deduplicate
    twin_pair_set = set(twin_pair_list)

    if (len(twin_pair_set) == 0):   
        return values
    

    # Eliminate the naked twins as possibilities for their peers
    
    for x,y in twin_pair_set:
        replace_candidate_boxes = peers[x] & peers[y]   
        for box in replace_candidate_boxes: 
            if any ( box in t for t in twin_pair_set ):
                return values
            value = values[box].replace(values[x][0],'').replace(values[x][1],'')
            values = assign_value(values, box , value)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return naked_twins(grid)
	
if __name__ == '__main__':
    
   display(naked_twins_test_1)
   print ('\n')
   display(solve(naked_twins_test_1))