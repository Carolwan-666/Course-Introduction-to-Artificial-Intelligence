#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

A propagator is a function with the following template:
    propagator(csp, newly_instaniated_variable=None)
        ...
        returns (True/False, [(Variable, Value),(Variable,Value),...])
        
    csp is a CSP object, which the propagator can use to get access to
    the variables and constraints of the problem
    
    newly_instaniated_variable is an optional argument;
        if it is not None, then:
            newly_instaniated_variable is the most recently assigned variable
        else:
            the propagator was called before any assignment was made
    
    the prop returns True/False and a list of variable-value pairs;
        the former indicates whether a DWO did NOT occur,
        and the latter specifies each value that was pruned
     
The propagator SHOULD NOT prune a value that has already been pruned
or prune a value twice

In summary, this is what the propagator must do:

    If newly_instantiated_variable = None
      
        for plain backtracking;
            we do nothing...return true, []

        for forward checking;
            we check all unary constraints of the CSP
            
        for gac;
            we establish initial GAC by initializing the GAC queue
            with all constaints of the CSP


     If newly_instantiated_variable = a variable V
      
         for plain backtracking;
            we check all constraints with V that are fully assigned
            (use csp.get_cons_with_var)

         for forward checking;
            we check all constraints with V that have one unassigned variable

         for gac;
            we initialize the GAC queue with all constraints containing V
   '''


def prop_BT(csp, newVar=None):

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    #IMPLEMENT
    prus = []
    cons = const(csp, newVar)
    for c in cons:
        if c.get_n_unasgn() == 1: # unary constraints of the CSP
            uns_var = c.get_unasgn_vars()[0]
            f, p = prune_FC(c, uns_var)
            prus.extend(p)
            if f is False:
                return f, prus
            else:
                continue
    return True, prus


def prune_FC(c, uns_var):
    pruned = []
    for val in uns_var.cur_domain():
        scp_vars = c.get_scope()
        i = 0
        v = []
        while i < len(scp_vars):
            scp_var = scp_vars[i]
            if scp_var.is_assigned():  # var in scope is assigned
                v.append(scp_var.get_assigned_value())
                i += 1
                continue
            v.append(val)  # var in scope is not assigned
            i += 1
        valid = c.check(v)
        if not valid:
            pr = (uns_var, val)
            if pr not in pruned:
                pruned.append(pr)
                uns_var.prune_value(val)
    flag = True
    if uns_var.cur_domain_size() == 0:
        flag = False
    return flag, pruned


def prop_GAC(csp, newVar=None):
    #IMPLEMENT
    cons = const(csp, newVar)
    return prune_GAC(csp, cons)


def prune_GAC(csp, q):
    pruned = []
    while q != []: # while Q ≠ ∅do:
        con = q.pop(0)
        scp = con.get_scope()
        ##
        for v in scp:
            for val in v.cur_domain():
                # if not Satisfiable(C,V,v)
                if not con.has_support(v, val):
                    pruned.append((v, val))
                    v.prune_value(val)
                    # if current domain is empty, return DWO
                    if v.cur_domain_size() == 0:
                        return False, pruned
                    else:
                        for c in csp.get_cons_with_var(v):
                            # loop the cons of current variable
                            if v in scp and c not in q:
                                q.append(c)
    return True, pruned


def const(csp, newVar):

    if newVar is None:
        return csp.get_all_cons()
    else:
        return csp.get_cons_with_var(newVar)




