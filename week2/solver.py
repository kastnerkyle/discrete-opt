#!/usr/bin/python
# -*- coding: utf-8 -*-

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    fl = lines[0].split()
    item_count = int(fl[0])
    capacity = int(fl[1])

    weights = []
    values = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    weights = tuple(weights)
    values = tuple(values)

    from dp_knapsack import solve_dp
    r = solve_dp(weights, values, capacity)

    value = r[0]
    indices = r[1]
    taken = [0] * len(weights)
    for i in indices:
        taken[i] = 1

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

