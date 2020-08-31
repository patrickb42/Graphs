"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def __iter__(self):
        pass

    def breadth_first_iter(self, starting_vertex):
        visited = set()
        need_to_visit = Queue()
        if starting_vertex not in self.vertices:
            raise Exception(f'vertex "{starting_vertex}" not in graph')
        cur_vertex = starting_vertex

        def add_to_queue(target):
            nonlocal visited
            nonlocal need_to_visit
            for vertex in target:
                if vertex not in visited:
                    visited.add(vertex)
                    need_to_visit.enqueue(vertex)

        add_to_queue(self.vertices[cur_vertex])
        yield cur_vertex
        visited.add(cur_vertex)
        while need_to_visit.size() > 0:
            cur_vertex = need_to_visit.dequeue()
            add_to_queue(self.vertices[cur_vertex])
            yield cur_vertex

    def depth_first_stack_iter(self, starting_vertex):
        class State:
            def __init__(self, vertex, remaining_neighbors):
                self.vertex = vertex
                self.remaining_neighbors = remaining_neighbors

        visited = set()
        history = Stack()

        if starting_vertex not in self.vertices:
            raise Exception(f'vertex "{starting_vertex}" not in graph')

        cur_state = State(starting_vertex, set(self.vertices[starting_vertex]))

        yield cur_state.vertex
        visited.add(cur_state.vertex)

        def set_next_state():
            nonlocal cur_state
            nonlocal history
            found_next = False
            while not found_next:
                cur_state.remaining_neighbors = cur_state.remaining_neighbors.difference(visited)
                if len(cur_state.remaining_neighbors) == 0:
                    cur_state = history.pop()
                    if cur_state is None:
                        return False
                else:
                    history.push(cur_state)
                    next_vertex = cur_state.remaining_neighbors.pop()
                    visited.add(next_vertex)
                    cur_state = State(
                        next_vertex,
                        self.vertices[next_vertex].difference(visited),
                    )
                    found_next = True
            return found_next

        while set_next_state():
            yield cur_state.vertex

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id in self.vertices:
            raise Exception(f'vertex "{vertex_id}" already exists in graph')
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        error: str = None
        TEMPLATE = 'vertex "{}" is not in graph'
        if v1 not in self.vertices:
            error = TEMPLATE.format(v1)
        if v2 not in self.vertices:
            error = TEMPLATE.format(v2) if error == ''\
                else f'{error} and {TEMPLATE.format(v2)}'
        if error:
            raise Exception(error)
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return list(self.vertices[vertex_id])

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        for vertex in self.breadth_first_iter(starting_vertex):
            print(vertex)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        for vertext in self.depth_first_stack_iter(starting_vertex):
            print(vertext)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex not in self.vertices:
            return

        visited = set()

        def print_next_vertex(cur_vertex):
            nonlocal visited
            print(cur_vertex)
            visited.add(cur_vertex)
            for next_vertex in self.vertices[cur_vertex]:
                if next_vertex not in visited:
                    print_next_vertex(next_vertex)

        print_next_vertex(starting_vertex)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        if starting_vertex not in self.vertices:
            raise Exception(f'vertex "{starting_vertex}" not in graph')
        elif destination_vertex not in self.vertices:
            raise Exception(f'vertex "{destination_vertex}" not in graph')

        encountered_vertices = set()
        need_to_visit = Queue()
        cur_vertex = starting_vertex
        cur_path = []
        need_to_visit.enqueue((cur_vertex, cur_path))
        while need_to_visit.size() > 0:
            (cur_vertex, cur_path) = need_to_visit.dequeue()
            cur_path.append(cur_vertex)
            if cur_vertex == destination_vertex:
                return cur_path
            for vertex in self.vertices[cur_vertex].difference(encountered_vertices):
                encountered_vertices.add(vertex)
                need_to_visit.enqueue((vertex, cur_path.copy()))
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        if starting_vertex not in self.vertices:
            raise Exception(f'vertex "{starting_vertex}" not in graph')
        elif destination_vertex not in self.vertices:
            raise Exception(f'vertex "{destination_vertex}" not in graph')

        visited = set()
        history = Stack()

        cur_vertex = starting_vertex
        cur_path = [cur_vertex]
        cur_vertex_remaining_neighbors = self.vertices[cur_vertex]
        found_path = False

        history.push((cur_vertex, cur_path.copy(), cur_vertex_remaining_neighbors))

        def set_next_state():
            nonlocal history
            nonlocal cur_vertex
            nonlocal cur_path
            nonlocal cur_vertex_remaining_neighbors
            nonlocal found_path

            found_next = False
            while not found_next:
                cur_vertex_remaining_neighbors = cur_vertex_remaining_neighbors.difference(visited)
                if len(cur_vertex_remaining_neighbors) == 0:
                    cur_state = history.pop()
                    if cur_state is None:
                        return False
                    (cur_vertex, cur_path, cur_vertex_remaining_neighbors) = cur_state
                else:
                    history.push((cur_vertex, cur_path.copy(), cur_vertex_remaining_neighbors))
                    next_vertex = cur_vertex_remaining_neighbors.pop()
                    visited.add(next_vertex)
                    cur_vertex = next_vertex
                    cur_path.append(cur_vertex)
                    cur_vertex_remaining_neighbors = self.vertices[cur_vertex].difference(visited)
                    found_next = True
            return found_next

        while set_next_state():
            if cur_vertex == destination_vertex:
                return cur_path

        return None

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if starting_vertex not in self.vertices:
            raise Exception(f'vertex "{starting_vertex}" not in graph')
        elif destination_vertex not in self.vertices:
            raise Exception(f'vertex "{destination_vertex}" not in graph')

        visited = set()
        found = False

        def next_vertex(cur_vertex, cur_path, neighbors):
            nonlocal found
            if cur_vertex == destination_vertex:
                found = True
                cur_path.append(cur_vertex)
                return cur_path
            visited.add(cur_vertex)
            for vertex in neighbors:
                path_arg = cur_path.copy()
                path_arg.append(cur_vertex)
                if vertex not in visited:
                    result = next_vertex(vertex, path_arg, self.vertices[vertex].difference(visited))
                if found:
                    return result

        return next_vertex(starting_vertex, [], self.vertices[starting_vertex])

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    # '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
