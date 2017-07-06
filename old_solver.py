#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
def greedy(weights, values, limit):
    #Take items in order until full
    w = 0.
    v = 0.
    t = np.zeros(len(weights))
    for i in range(len(weights)):
        if (weights[i] + w) <= limit:
            t[i] = 1
            v += values[i]
            w += weights[i]
    return w, v, t

def greedy_ratio(weights, values, limit):
    #Arrange by maximum ratio
    d = weights / values
    si = np.argsort(d)[::-1]
    w_s = weights[si]
    v_s = values[si]

    #Weights to invert the output of greedy solution
    #because input is fed in sorted by weight:value ratio
    ti = np.argsort(si)

    #Get back weight and value for greedy ratio
    #Result needs to be resorted due to getting sorted input
    w, v, t_u = greedy(w_s, v_s, limit)
    t = t_u[ti]
    return w, v, t

def revised_simplex(penalty, minimize, limits, inequality=True, eps=1E-6):
    #For now, translate variables to algorithmic form
    #Good resource here
    #www.cise.ufl.edu/research/sparse/Morgan/chapter2.htm
    #Multiply by -1 or won't solve!
    c = -1 * np.atleast_1d(minimize)
    A = np.atleast_2d(penalty)
    b = np.atleast_1d(limits)

    if inequality:
        #Add slack variables since limit specifies an inequality
        A = np.hstack((A, np.eye(b.shape[0])))
        c = np.hstack((c, [0] * b.shape[0] + [1]))
        if A.shape[0] != c.shape:
            #Handle edge case with only 1 constraint
            A = np.hstack((A, [[0]]))

    #Really need best feasible solution calculation here
    basis = np.arange(b.shape[0])
    while True:
        #Get nonbasis columns from basis
        nonbasis = np.arange(A.shape[1])
        nonbasis[basis] = -1.
        nonbasis = nonbasis[nonbasis >= 0]

        #Calculate basis and nonbasis matrices
        B = np.atleast_2d(A[:, basis])
        V = np.atleast_2d(A[:, nonbasis])

        #Calculate basis inverse
        Binv = np.linalg.inv(B)
        d = np.dot(Binv, b)
        ct = c[nonbasis] - np.dot(np.dot(c[basis], Binv), V)

        #Get minimum and associated index
        j = np.argmin(ct)
        cj = np.min(ct)

        #If value >= 0, then this solution is near optimal
        if cj >= -eps:
            t = np.zeros(c.shape)
            t[basis] = d
            if inequality:
                t = t[:len(penalty)]
            w = np.dot(penalty, t)
            v = np.dot(minimize, t)
            return w, v, t

        #Find smallest positive ratio and update basis
        w = Binv * A[:, j]
        t = np.where(w > eps)[0]
        r = d[t] / w[t]
        i = np.argmin(r)
        basis[t[i]] = j

def branch_and_bound(weights, values, limit,
                     m_weights=None, m_values=None, t=[]):
    if m_weights is None:
        m_weights = weights.copy()
    if m_values is None:
        m_values = values.copy()
    if len(t) < len(weights):
        #Bounds check for lhs
        nw, nv, nt = branch_and_bound(weights, values, limit,
                             m_weights[1:], m_values[1:], t + [0])
        #Bounds check for rhs
        tw, tv, tt = branch_and_bound(weights, values, limit,
                             m_weights[1:], m_values[1:], t + [1])

        if tv > nv and tw <= limit:
            w, v, t = (tw, tv, tt)
        else:
            w, v, t = (nw, nv, nt)
    else:
        w = np.dot(weights, np.array(t))
        v = np.dot(values, np.array(t))
        #t is already fleshed out
    return w, v, t

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    #values, weight
    items = np.zeros((item_count, 2))
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items[i - 1, :] = np.array([int(parts[0]), int(parts[1])])

    values = v = items[:, 0]
    weights = w = items[:, 1]
    bound = b = capacity

    #Trivial solution
    #w, v, t = greedy(w, v, b)

    #Almost trivial solution
    #w, v, t = greedy_ratio(w, v, b)

    #Revised simplex for LP
    #print revised_simplex(w, v, b)

    #Better solution
    w, v, t = branch_and_bound(w, v, b)

    # taken needs to be a list
    # value needs to be a list as well
    taken = t
    value = v

    # prepare the solution in the specified output format
    output_data = str(int(value)) + ' ' + ' ' + str(0) + '\n'
    output_data += ' '.join(map(lambda x: str(int(x)), taken))
    return output_data


import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'
