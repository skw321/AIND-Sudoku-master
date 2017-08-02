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


naked_twins_test_1 = {"G7": "1569", "G6": "134568", "G5": "13568", "G4": "134568", "G3": "2", "G2": "34589", "G1": "7", "G9": "5689", "G8": "15", "C9": "56", "C8": "3", "C3": "7", "C2": "1245689", "C1": "1245689", "C7": "2456", "C6": "1245689", "C5": "12568", "C4": "1245689", "E5": "4", "E4": "135689", "F1": "1234589", "F2": "12345789", "F3": "34589", "F4": "123589", "F5": "12358", "F6": "123589", "F7": "14579", "F8": "6", "F9": "3579", "B4": "1234567", "B5": "123567", "B6": "123456", "B7": "8", "B1": "123456", "B2": "123456", "B3": "345", "B8": "9", "B9": "567", "I9": "578", "I8": "27", "I1": "458", "I3": "6", "I2": "458", "I5": "9", "I4": "124578", "I7": "3", "I6": "12458", "A1": "2345689", "A3": "34589", "A2": "2345689", "E9": "2", "A4": "23456789", "A7": "24567", "A6": "2345689", "A9": "1", "A8": "4", "E7": "159", "E6": "7", "E1": "135689", "E3": "3589", "E2": "135689", "E8": "15", "A5": "235678", "H8": "27", "H9": "4", "H2": "3589", "H3": "1", "H1": "3589", "H6": "23568", "H7": "25679", "H4": "235678", "H5": "235678", "D8": "8", "D9": "3579", "D6": "123569", "D7": "14579", "D4": "123569", "D5": "12356", "D2": "12345679", "D3": "3459", "D1": "1234569"}


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
        if values[x] == values[y]:   
            replace_candidate_boxes = peers[x] & peers[y]  
            for box in replace_candidate_boxes:
                for digit in values[x]:
                    value = values[box].replace(digit,'') 
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