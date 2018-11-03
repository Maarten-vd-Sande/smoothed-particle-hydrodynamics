import math
import itertools


class SpatialHash:
    """
    Simple spatial-hash.
    """
    def __init__(self, width, height, cellsize):
        self.width = width
        self.height = height
        self.cellsize = cellsize

        self.cells = [[Node(-1) for _ in range(math.ceil(height / cellsize))] for _ in range(math.ceil(width / cellsize))]
        self.xcells = len(self.cells)
        self.ycells = len(self.cells[0])
        self.nodes = {}

    def coords_to_index(self, coords):
        return int(coords[0] // self.cellsize), int(coords[1] // self.cellsize)

    def neighbours(self, coords):
        location = self.coords_to_index(coords)
        for dx, dy in itertools.product(range(-1, 2), range(-1, 2)):
            node = self.cells[location[0] + dx][location[1] + dy].next
            while node is not None:
                yield node.id
                node = node.next

    def move(self, id, new_coords):
        node = self.nodes.get(id)
        if node is None:
            node = Node(id)
            self.nodes[id] = node

        location = self.coords_to_index(new_coords)
        node.attach(self.cells[location[0]][location[1]])


class Node:
    """
    Nodes for a linked-list
    """
    def __init__(self, id):
        self.id = id

        self.prev = None
        self.next = None

    def attach(self, start):
        # remove contacts
        if self.prev is not None:
            self.prev.next = self.next
            self.prev = None
        if self.next is not None:
            self.next.prev = self.prev
            self.next = None

        # attact to front
        self.next = start.next
        if self.next:
            self.next.prev = self

        self.prev = start
        start.next = self
        pass

