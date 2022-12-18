#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = warehouse_binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the warehouse.

The grid-only models do not need to encode the cage constraints.

1. warehouse_binary_ne_grid
    - A model of the warehouse problem w/o room constraints built using only 
      binary not-equal constraints for the row/column constraints.

2. warehouse_nary_ad_grid
    - A model of the warehouse problem w/o room constraints built using only n-ary 
      all-different constraints for the row/column constraints. 

3. warehouse_full_model
    - A model of the warehouse problem built using either the binary not-equal or n-ary
      all-different constraints for the row/column constraints.
'''
from cspbase import *
import itertools


def check(i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj
       respectively. Used to find satisfying tuples.
    '''
    return i != j

def bcheck(row_num, m):

    sub_cons = []
    dom = []
    for i in range(row_num):
        dom.append(i + 1)

    for i in range(len(dom)):
        for qi in range(len(dom)):
            for qj in range(qi + 1, row_num):
                con = Constraint("C(V({},V{})".format(qi+1, qj+1),
                                 [m[i][qi], m[i][qj]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if check(t[0], t[1]):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                sub_cons.append(con)
    return sub_cons


def warehouse_binary_ne_grid(warehouse_grid):
    ##IMPLEMENT
    dom = []
    row_num = warehouse_grid[0][0]
    # create the board
    m = []
    for i in range(row_num):
        m.append([1] * row_num)  #
        dom.append(i+1)

    vars = []
    for b in warehouse_grid[1:]:
        for r in b[:-2]:
            position = str(r)
            y = int(position[0]) #col
            x = int(position[1]) #row
            v = Variable('V({},{})'.format(y, x), dom)
            vars.append(v)
            # filling the matrix
            m[x-1][y-1] = v

    cons = []
    sub_con1 = bcheck(row_num, m)
    cons.extend(sub_con1)
    tr_m = [*zip(*m)]
    sub_con2 = bcheck(row_num, tr_m)
    cons.extend(sub_con2)

    # not-equal
    for b in warehouse_grid[1:]:
        if b[-2] == 0:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x-1][y-1])
            con = Constraint("Con({})".format("="), scp)
            sat_tuples = []
            for t in itertools.product(scp[0].cur_domain()):
                if t[0] == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 1:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x-1][y-1])
            con = Constraint("Con({})".format("+"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if sum(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 2:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("min"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if min(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 3:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("max"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if max(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("binary", vars)
    for c in cons:
        csp.add_constraint(c)
    return csp, m


def warehouse_nary_ad_grid(warehouse_grid):
    ##IMPLEMENT
    dom = []
    row_num = warehouse_grid[0][0]
    # create the board
    m = []
    for i in range(row_num):
        m.append([1] * row_num)  #
        dom.append(i + 1)

    vars = []
    for b in warehouse_grid[1:]:
        for r in b[:-2]:
            position = str(r)
            y = int(position[0])  # col
            x = int(position[1])  # row
            v = Variable('V({},{})'.format(y, x), dom)
            vars.append(v)
            # filling the matrix
            m[x - 1][y - 1] = v

    cons = []
    #row
    for i in range(row_num):
        row = m[i]
        c1 = Constraint("row{}".format(i), row)
        sat_tuples = []
        for t in itertools.product(*[var.cur_domain() for var in row]):
            if len(set(t)) == row_num:
                sat_tuples.append(t)
        c1.add_satisfying_tuples(sat_tuples)
        cons.append(c1)
    #col
    for i in range(row_num):
        col = [row[i] for row in m]
        c2 = Constraint("col{}".format(i), col)
        sat_tuples = []
        for t in itertools.product(*[var.cur_domain() for var in col]):
            if len(set(t)) == row_num:
                sat_tuples.append(t)
        c2.add_satisfying_tuples(sat_tuples)
        cons.append(c2)

    for b in warehouse_grid[1:]:
        if b[-2] == 0:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x-1][y-1])
            con = Constraint("Con({})".format("="), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if t[0] == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 1:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x-1][y-1])
            con = Constraint("Con({})".format("+"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if sum(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 2:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("min"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if min(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 3:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("max"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if max(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("nary", vars)
    for c in cons:
        csp.add_constraint(c)
    return csp, m


def warehouse_full_model(warehouse_grid):
    dom = []
    row_num = warehouse_grid[0][0]
    # create the board
    m = []
    for i in range(row_num):
        m.append([1] * row_num)  #
        dom.append(i + 1)

    vars = []
    for b in warehouse_grid[1:]:
        for r in b[:-2]:
            position = str(r)
            y = int(position[0])  # col
            x = int(position[1])  # row
            v = Variable('V({},{})'.format(y, x), dom)
            vars.append(v)
            # filling the matrix
            m[x - 1][y - 1] = v

    cons = []
    sub_con1 = bcheck(row_num, m)
    cons.extend(sub_con1)
    tr_m = [*zip(*m)]
    sub_con2 = bcheck(row_num, tr_m)
    cons.extend(sub_con2)

    # row
    for i in range(row_num):
        row = m[i]
        c1 = Constraint("row{}".format(i), row)
        sat_tuples = []
        for t in itertools.product(*[var.cur_domain() for var in row]):
            if len(set(t)) == row_num:
                sat_tuples.append(t)
        c1.add_satisfying_tuples(sat_tuples)
        cons.append(c1)
    # col
    for i in range(row_num):
        col = [row[i] for row in m]
        c2 = Constraint("col{}".format(i), col)
        sat_tuples = []
        for t in itertools.product(*[var.cur_domain() for var in col]):
            if len(set(t)) == row_num:
                sat_tuples.append(t)
        c2.add_satisfying_tuples(sat_tuples)
        cons.append(c2)

    # not-equal
    for b in warehouse_grid[1:]:
        if b[-2] == 0:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("="), scp)
            sat_tuples = []
            for t in itertools.product(scp[0].cur_domain()):
                if t[0] == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 1:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("+"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if sum(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 2:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("min"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if min(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

        elif b[-2] == 3:
            scp = []
            for r in b[:-2]:
                position = str(r)
                y = int(position[0])  # col
                x = int(position[1])  # row
                scp.append(m[x - 1][y - 1])
            con = Constraint("Con({})".format("max"), scp)
            sat_tuples = []
            for t in itertools.product(*[var.cur_domain() for var in scp]):
                if max(t) == b[-1]:
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    csp = CSP("full", vars)
    for c in cons:
        csp.add_constraint(c)
    return csp, m