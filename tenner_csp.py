#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

################ Helper Functions #########################

def init_vars(initial_tenner_board):

    domain = []
    for i in range(10):
        domain.append(i)

    n_grid = initial_tenner_board[0]

    vars = []

    #Init variables
    for i in range(len(n_grid)):
        for j in range(len(n_grid[i])):
            if n_grid[i][j] == -1:
                vars.append(Variable('V{},{}'.format(i,j), domain))
            else:
                vars.append(Variable('V{},{}'.format(i,j), [n_grid[i][j]]))

    return vars




def get_col_cons(initial_tenner_board, variable_array):
    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]

    cons = []

    for j in range(len(n_grid[0])):
        vars = []
        for i in range(len(n_grid)):
            vars.append(variable_array[j + len(n_grid)*i])
        con = Constraint("Col_C_{}".format(j),vars)
        sum = last_row[j]
        tuples = []
        domains = []

        for variable in vars:
            domains.append(variable.domain())
        for t in itertools.product(*domains):
            if sum(t) == sum:
                   tuples.append(t)
        con.add_satisfying_tuples(tuples)
        cons.append(con)

    return cons

def get_row_cons(initial_tenner_board, binary, variable_array):
    n_grid = initial_tenner_board[0]
    last_row = initial_tenner_board[1]

    cons = []
    if binary == True:
        for row_num in range(len(n_grid)):
            row_vars = variable_array[len(n_grid[0])*row_num: len(n_grid[0])*(row_num+1)]
            for i in range(len(row_vars)):
                for j in range(i+1, len(row_vars)):
                    con = Constraint("Col_R_{}{}".format(i,j),vars)
                    tuples = []
                    for t in itertools.product(row_vars[i].domain(), row_vars[j].domain()):
                        if t[0] != t[1]:
                            tuples.append(t)
                    con.add_satisfying_tuples(tuples)
                    cons.append(con)

    else:
        print("lol")
    return cons

def get_equality_cons(initial_tenner_board, variable_array):
    # rows already satisfied
    max_cols = 9
    max_rows = len(initial_tenner_board[0])
    cons = []
    spot = (0, 0)

    for row in range(len(initial_tenner_board[0])):
        for col in range(len(initial_tenner_board[0][0])):
            index = 10*row + col
            n = [variable_array[index]]
            if row - 1 > 0:
                n.append(variable_array[10*(row-1) + col])
                if col - 1 > 0:
                    n.append(variable_array[10*(row-1) + (col-1)])
                if col + 1 < max_cols:
                    n.append(variable_array[10*(row-1) + (col+1)])
            if row + 1 < max_rows:
                n.append(variable_array[10*(row+1) + col])
                if col - 1 > 0:
                    n.append(variable_array[10*(row+1) + (col-1)])
                if col + 1 < max_cols:
                    n.append(variable_array[10*(row+1) + (col+1)])

    for i in range(len(n)):
        for j in range(i+1, len(n)):
            con = Constraint("Eq_{}{}".format(i,j),vars)
            tuples = []
            for t in itertools.product(n[i].domain(), n[j].domain()):
                if t[0] != t[1]:
                    tuples.append(t)
            con.add_satisfying_tuples(tuples)
            cons.append(con)



    return cons

###########################################################

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 7.


       The input board is specified as a pair (n_grid, last_row).
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid.
       If a -1 is in the list it represents an empty cell.
       Otherwise if a number between 0--9 is in the list then this represents a
       pre-set board position. E.g., the board

       ---------------------
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists

       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]


       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.

       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each
       column.
    '''


    # print(initial_tenner_board)
    variable_array = init_vars(initial_tenner_board)
    tenner_csp = CSP("model 1", variable_array)

    cons = get_col_cons(initial_tenner_board, variable_array) + get_row_cons(initial_tenner_board, True, variable_array) + get_equality_cons(initial_tenner_board, variable_array)

    for c in cons:
        tenner_csp.add_constraint(c)


    return tenner_csp, variable_array
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.

       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary
       contstraints to encode contiguous cells (including diagonally contiguous
       cells), however. Each -ary constraint is over more
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''
    variable_array = init_vars(initial_tenner_board)
    tenner_csp = CSP("model 2", variable_array)

    cons = get_col_cons(initial_tenner_board, variable_array) + get_row_cons(initial_tenner_board, False, variable_array) + get_equality_cons(initial_tenner_board, variable_array)

    for c in cons:
        tenner_csp.add_constraint(c)

    return tenner_csp, variable_array
