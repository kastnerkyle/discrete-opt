# https://codereview.stackexchange.com/questions/44421/knapsack-branch-and-bound-forward-filter
import Queue
from collections import namedtuple
import numpy as np
import heapq

class Node(object):
    def __init__(self, level, value, weight, taken):
        self.level = level
        self.value = value
        self.weight = weight
        self.taken = taken

    def __repr__(self):
        return str((self.level, self.value, self.weight, self.taken))


class Knapsack(object):
    def __init__(self, values, weights, capacity):
        self.values = values
        self.weights = weights
        assert len(self.values) == len(self.weights)
        self.capacity = capacity


    def _greedy(self, at, v_offset, w_offset, e_list):
        vv = self.values[at:]
        ww = self.weights[at:]
        ii = np.argsort([float(vvi) / wwi for vvi, wwi in zip(vv, ww)])[::-1]
        ro_vv = [vv[i] for i in ii]
        ro_ww = [ww[i] for i in ii]
        cur_wsum = w_offset
        cur_vsum = v_offset
        taken = []
        for idx, (rov, row) in enumerate(zip(ro_vv, ro_ww)):
            if cur_wsum + row <= self.capacity:
                taken.append(idx)
                cur_vsum += rov
                cur_wsum += row
        mapback = [ii[t] for t in taken]
        return Node(at, cur_vsum, cur_wsum, e_list + list(mapback))


    def _linear_relaxation(self, at, cv, cw):
        weight = cw
        value = cv
        vv = self.values[at:]
        ww = self.weights[at:]
        ii = np.argsort([float(vvi) / wwi for vvi, wwi in zip(vv, ww)])[::-1]
        ro_vv = [vv[i] for i in ii]
        ro_ww = [ww[i] for i in ii]

        for (rov, row) in zip(ro_vv, ro_ww):
            if row + weight <= self.capacity:
                value += rov
                weight += row
            else:
                # finalize fractional value
                dw = (self.capacity - weight)
                frac = float(dw) / row
                weight += dw
                dv = frac * rov
                value += dv
        return value


    def solve(self, stype="depth"):
        root = Node(0, 0, 0, [])
        best = root
        best_lb = self._greedy(0, 0, 0, [])
        best_lbv = best_lb.value
        best_ubv = self._linear_relaxation(0, 0, 0)
        # placeholder for non-binary trees
        options = [0]

        if stype == "depth":
            el = [root]
            def push(i, p=None):
                el.append(i)

            def pop():
                return el.pop()
        elif stype == "breadth":
            el = [root]
            def push(i, p=None):
                el.append(i)

            def pop():
                return el.pop(0)
        elif stype == "best":
            # assume maximization
            el = [(0, root)]
            heapq.heapify(el)
            def push(i, p=None):
                heapq.heappush(el, (-p, i))

            def pop():
                return heapq.heappop(el)[1]
        else:
            raise ValueError("Unknown solver type")

        while len(el) > 0:
            for o in range(len(options)):
                current = pop()
                index = current.level

                if current.value >= best.value:
                    best = current

                if index < len(self.values):
                    if current.weight + self.weights[index] <= self.capacity:
                        taken = list(current.taken)
                        taken.append(index)

                        take = Node(index + 1, current.value + self.values[index],
                                    current.weight + self.weights[index], list(taken))
                        if take.value > best.value:
                            best = take
                            best_lb = self._greedy(index + 1, best.value, best.weight, best.taken)
                            best_lbv = best_lb.value
                            lb = best_lb
                            lbv = best_lbv
                        else:
                            lb = self._greedy(index + 1, take.value, take.weight, list(taken))
                            lbv = lb.value

                        if lbv >= best_lbv:
                            best = take
                            best_lb = lb
                            best_lbv = lbv
                            push(take, lbv)
                        else:
                            ubv = self._linear_relaxation(index + 1, take.value, take.weight)
                            if ubv >= best_ubv:
                                best_ubv = ubv
                                push(take, lbv)

                    not_taken = list(current.taken)
                    dont = Node(index + 1, current.value, current.weight, list(not_taken))
                    lb = self._greedy(index + 1, dont.value, dont.weight, list(not_taken))
                    lbv = lb.value
                    if lbv >= best_lbv:
                        best = dont
                        best_lb = lb
                        best_lbv = lbv
                        push(dont, lbv)
                    else:
                        ubv = self._linear_relaxation(index + 1, dont.value, dont.weight)
                        if ubv >= best_ubv:
                            best_ubv = ubv
                            push(dont, lbv)
        return best


if __name__ == "__main__":
    values = [45, 48, 35]
    weights = [5, 8, 3]
    capacity = 10
    k = Knapsack(values, weights, capacity)
    r = k.solve()
    from IPython import embed; embed(); raise ValueError()
