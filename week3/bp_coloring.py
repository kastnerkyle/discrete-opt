import copy

class Node(object):
    def __init__(self, level, next_node_id, node_lookup):
            # other_nodes is list of tuples
            self.level = level
            self.next_node_id = next_node_id
            self.node_lookup = copy.deepcopy(node_lookup)

    def __repr__(self):
        return str((self.level, self.next_node_id, self.node_lookup))


class Coloring(object):
    def __init__(self, n_colors, connectivity_graph):
        self.n_colors = n_colors
        self.connectivity_graph = connectivity_graph
        all_values = connectivity_graph.values()
        self.all_nodes = set(connectivity_graph.keys() + [vi for v in all_values for vi in v])
        self.color_set = [i for i in range(self.n_colors)]

    def valid_color(self, node, color, current_lookup):
        gg = self.connectivity_graph
        if node in gg:
            neighbors = gg[node]
            neighbor_colors = [current_lookup[n] for n in neighbors
                               if n in current_lookup]
            if color in neighbor_colors:
                return False
        return True

    def solve(self, stype="depth", quit="first"):
        # choose node and color to start with at random?
        el = []

        def push(i):
            el.append(i)

        def pop():
            return el.pop()

        # all possible starting nodes - this may not be ideal
        for v in self.all_nodes:
            n = Node(0, v, {})
            push(n)

        soln = []

        break_while = False
        while len(el) > 0 and break_while is False:
            options = self.color_set
            current = pop()
            for ni, o in enumerate(options):
                index = current.level
                current_next_id = current.next_node_id
                current_lookup = copy.deepcopy(current.node_lookup)
                # current_next_id should never be in the lookup
                if self.valid_color(current_next_id, o, current_lookup):
                    current_lookup[current_next_id] = o
                    remaining = self.all_nodes - set(current_lookup.keys())
                    if len(remaining) > 0:
                        for v in remaining:
                            new_n = Node(index + 1, v, current_lookup)
                            push(new_n)
                    else:
                        # final check
                        if self.valid_color(current_next_id, o, current_lookup):
                            final_lookup = copy.deepcopy(current_lookup)
                            final_lookup[current_next_id] = o
                            new_n = Node(index + 1, None, final_lookup)
                            soln.append(new_n)
                            if quit == "first":
                                break_while = True
                                break
        assert len(soln) > 0
        return soln


if __name__ == "__main__":
    g = {k: [] for k in range(4)}
    g[0] = [1]
    g[1] = [0, 2, 3]
    g[2] = [1]
    g[3] = [1]

    c = Coloring(3, g)
    r = c.solve()
    print(r)
