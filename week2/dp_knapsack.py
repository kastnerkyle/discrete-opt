import numpy as np

class memoize(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result

@memoize
def dp(k, j, w, v):
    # k is knapsack size
    # j is index (0 indexed)
    # w is weight list
    # v is value list
    if j == -1:
        return 0, ()
    elif w[j] <= k:
        p1 = dp(k, j - 1, w, v)
        p2 = dp(k - w[j], j - 1, w, v)
        amx = np.argmax([p1[0], v[j] + p2[0]])
        r = [p1[0], v[j] + p2[0]]
        rt = [p1[1], p2[1] + (j,)]
        return r[amx], rt[amx]
    else:
        return dp(k, j - 1, w, v)


def solve_dp(weights, values, max_weight):
    # weights are tuple
    # values are tuple
    # max_weight is max knapsack weight
    best = (-1, ())
    for ji in range(-1, len(weights)):
        for ki in range(max_weight + 1):
            r = dp(ki, ji, weights, values)
            if r[0] > best[0]:
                best = r
    return best

'''
# example 1
values = (5, 6, 3)
weights = (4, 5, 2)
max_k = 9
print(solve_dp(weights, values, max_k))
'''

'''
# example 2
values = (16, 19, 23, 28)
weights = (2, 3, 4, 5)
max_k = 7
print(solve_dp(weights, values, max_k))
'''
