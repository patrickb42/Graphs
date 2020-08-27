from typing import List, Dict, Set

from room import Room
from util import Queue

def find_path(starting_room: Room) -> List[str]:
    raw_path: List[Room] = [starting_room]
    visited: Set[Room] = set([starting_room])
    rooms_graph = build_graph(starting_room)
    rooms_set = set(rooms_graph.keys())
    shortest_routes: Dict[Room, Dict[Room, List[Room]]] = {
        room: get_shortest_routes(room) for room in rooms_graph
    }

    cur_room: Room = starting_room
    while len(rooms_set.difference(visited)) > 0:
        raw_path.extend(get_path_to_nearest_dead_end(cur_room, shortest_routes, visited))
        cur_room = raw_path[-1]
        visited.add(cur_room)
        raw_path.extend(get_path_to_nearest_unvisited(cur_room, shortest_routes, visited))
        cur_room = raw_path[-1]
        visited.add(cur_room)


    directional_path: List[str] = convert_rooms_path_to_direcctional(raw_path)

    return directional_path

def get_path_to_nearest_dead_end(
        starting_room: Room,
        shortest_routes: Dict[Room, Dict[Room, List[Room]]],
        visited: Set[Room],
) -> List[Room]:
    for cur_path in shortest_routes[starting_room].values():
        cur_visited = visited.copy().union(set(cur_path))
        cur_room = cur_path[-1]
        if cur_room not in cur_visited and is_dead_end(cur_room, cur_visited):
            return cur_path[1 : ]
    return []

def is_dead_end(room: Room, visited: Set[Room]):
    for direction in room.get_exits:
        if room.get_room_in_direction(direction) not in visited:
            return False
    return True

def get_path_to_nearest_unvisited(
        starting_room: Room,
        shortest_routes: Dict[Room, Dict[Room, List[Room]]],
        visited: Set[Room]
) -> List[Room]:
    for cur_path in shortest_routes[starting_room].values():
        cur_room = cur_path[-1]
        if cur_room not in visited:
            return cur_path[1 : ]
    return []

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
