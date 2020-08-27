from typing import Set, Dict, List

from graph import Graph
from util import Queue
from room import Room

def find_path(starting_room: Room):
    raw_path: List[Room] = [starting_room]
    visited: Set[Room] = set([starting_room])
    rooms_graph = build_graph(starting_room)
    rooms_set = set(rooms_graph.keys())
    shortest_routes: Dict[Room, Dict[Room, List[Room]]] = {
        room: get_shortest_routes(room) for room in rooms_graph
    }
    paths_weighted_values: Dict[List[Room], float] = init_weighted_paths(shortest_routes)
    # paths_weighted_values: Dict[List[Room], float] = {}

    while len(rooms_set.difference(visited)) > 0:
        next_target: Room = get_next_target(list(rooms_graph.keys()), shortest_routes, visited, paths_weighted_values)
        # print(f'next target room is {next_target.id}')
        # path_to_next = list(shortest_routes[raw_path[-1]][next_target])[1 : ] THIS SEEMS TO BE BROKEN
        raw_path.extend(path_to_next)
        # print(f'visiting: {path_to_next}')
        for room in path_to_next:
            visited.add(room)

    directional_path: List[str] = convert_rooms_path_to_direcctional(raw_path)

    return directional_path

def get_next_target(
        rooms: List[Room],
        shortest_routes: Dict[Room, Dict[Room, List[Room]]],
        visited: Set[Room],
        paths_weighted_values: Dict[List[Room], float],
):
    room_unweighted_values: Dict[Room, float]
    room_weighted_values: Dict[Room, float]

    room_unweighted_values = {
        room: get_average_path_unweighted_value(room,
                                                shortest_routes,
                                                visited,
                                               ) for room in rooms
    }

    room_weighted_values = {
        room: get_average_weighted_path_value(room,
                                              shortest_routes,
                                              room_unweighted_values,
                                              ) for room in rooms
    }

    for path in paths_weighted_values:
        total = 0.0
        for room in path:
            total += room_weighted_values[room]
        paths_weighted_values[path] = total / len(path)
        if paths_weighted_values[path] == 0:
            del paths_weighted_values[path]

    # return max(room_weighted_values, key=room_weighted_values.get)
    return max(paths_weighted_values, key=paths_weighted_values.get)

def get_shortest_routes(starting_room):
    shortest_routes: Dict[Room, List[Room]] = {}
    need_to_visit = Queue()
    visited: Set[Room] = set()

    need_to_visit.enqueue([starting_room])
    while need_to_visit.size() > 0:
        cur_path: List[Room] = need_to_visit.dequeue()
        cur_room = cur_path[-1]
        shortest_routes[cur_room] = tuple(cur_path)
        visited.add(cur_room)

        for direction in cur_room.get_exits():
            room: Room = cur_room.get_room_in_direction(direction)
            if room not in visited:
                next_path = cur_path.copy()
                next_path.append(room)
                need_to_visit.enqueue(next_path)

    return shortest_routes

def get_average_path_unweighted_value(
        room: Room,
        shortest_routes: Dict[Room, Dict[Room, List[Room]]],
        visited: Set[Room],
):
    total = 0.0
    paths = shortest_routes[room].values()

    for path in paths:
        for cur_room in path:
            total += 1.0 if cur_room not in visited else 0

    return total

def get_average_weighted_path_value(
        room: Room,
        shortest_routes: Dict[Room, Dict[Room, List[Room]]],
        room_unweighted_value: Dict[Room, float],
):
    total = 0.0
    paths = shortest_routes[room].values()

    for path in paths:
        for cur_room in path:
            total += room_unweighted_value[room]

    return total

def init_weighted_paths(shortest_routes: Dict[Room, Dict[Room, List[Room]]]):
    result: Dict[List[Room], float] = {}

    for shortest_path_to_rooms in shortest_routes.values():
        for path in shortest_path_to_rooms.values():
            result[path] = len(path)

    return result

def convert_rooms_path_to_direcctional(raw_path: List[Room]):
    directional_path: List[str] = []
    raw_path_iter = iter(raw_path)
    room = next(raw_path_iter)
    for next_room in raw_path_iter:
        if room.n_to == next_room:
            directional_path.append('n')
        elif room.s_to == next_room:
            directional_path.append('s')
        elif room.e_to == next_room:
            directional_path.append('e')
        else:
            directional_path.append('w')
        room = next_room
    return directional_path
        

def build_graph(starting_room: Room) -> Dict[Room, List[Room]]:
    need_to_visit = Queue()
    visited: Set[Room] = set()
    rooms_graph: Dict[Room, List[Room]] = {}

    need_to_visit.enqueue(starting_room)

    while need_to_visit.size() > 0:
        cur_room: Room = need_to_visit.dequeue()
        rooms_graph[cur_room] = []
        visited.add(cur_room)
        for direction in cur_room.get_exits():
            room = cur_room.get_room_in_direction(direction)
            if room is not None:
                rooms_graph[cur_room].append(room)
            if room not in visited:
                need_to_visit.enqueue(room)

    return rooms_graph

# def average_dist_to_all_rooms(starting_room: Room, rooms_graph: Dict[Room, List[Room]]):
#     cur_depth = 0
#     for room, neighbors in rooms_graph.items():
#         pass

# def get_average_shortest_path_len(starting_room: Room):
#     need_to_visit = Queue()
#     visited: Set[Room] = set()

#     depth = 0
#     unvisited_exit_found: False
#     path_count = 0
#     total_paths_depth = 0

#     for exit_direction in starting_room.get_exits():
#         target: Room = starting_room.get_room_in_direction(exit_direction)
#         if target not in visited:
#             unvisited_exit_found = True
#             need_to_visit.enqueue(target)
#     if not unvisited_exit_found:
#         path_count += 1
#         total_paths_depth += depth

#     # do this after everthing has been reached
#     room_scores

# rank all the rooms that are the hardest to get to by finding the average shorests route length relative to all other rooms
# find the shortest route to each unvisited room from where you are; get the average score per move for each path (visited rooms are worth 0)
