from graph import Graph
def earliest_ancestor(ancestors, starting_node):
    child_parent_association = {}

    for ancestor in ancestors:
        if ancestor[1] not in child_parent_association:
            child_parent_association[ancestor[1]] = set()
        child_parent_association[ancestor[1]].add(ancestor[0])

    longest_route_length = 0
    farthest_ancestor = -1

    def next_ancestor(cur_ancestor, cur_length):
        nonlocal longest_route_length
        nonlocal farthest_ancestor
        if cur_length >= longest_route_length:
            if cur_length > longest_route_length\
                    or (cur_length == longest_route_length\
                        and cur_ancestor < farthest_ancestor):
                longest_route_length = cur_length
                farthest_ancestor = cur_ancestor
        if cur_ancestor in child_parent_association:
            for ancestor in child_parent_association[cur_ancestor]:
                next_ancestor(ancestor, cur_length + 1)

    next_ancestor(starting_node, 0)

    return farthest_ancestor
