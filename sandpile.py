import random
import struct
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Coord:
    x: int
    y: int

def MakeGrid(x):
    return [[0 for _ in range(x)] for _ in range(x)]

def RandomCoord(grid):
    size = len(grid) - 1
    random.seed()
    return Coord(random.randint(0, size), random.randint(0, size))

def PlaceGrain(grid, coord):
    grid[coord.x][coord.y] += 1
    return grid

def WillFall(grid, coord):
    return grid[coord.x][coord.y] > MAXN

def NumOrNone(n, size):
    return n if n < size else None

def GetNeighbors(grid, coord):
    size = len(grid)
    return [
        Coord(NumOrNone(coord.x + 1, size), coord.y),
        Coord(coord.x, NumOrNone(coord.y + 1, size)),
        Coord(NumOrNone(coord.x - 1, size), coord.y),
        Coord(coord.x, NumOrNone(coord.y - 1, size)),
    ]

def Cascade(grid, coord, step):
    if WillFall(grid, coord):
        grid[coord.x][coord.y] -= 4
        Record[step] += 1
        for n in GetNeighbors(grid, coord):
            if n.x and n.y:
                grid = PlaceGrain(grid, n)
                return Cascade(grid, n, step)
    return grid

def Run(grid, steps):
    for step in range(steps):
        coord = RandomCoord(grid)
        grid = PlaceGrain(grid, coord)
        grid = Cascade(grid, coord, step)
    return grid

def ProcessRecord(rec, threshold):
    totals = defaultdict(int)
    for k,v in rec.items():
        if v > threshold:
            totals[v] += 1
    return totals

MAXN = 4
size = 20
steps = 10000
Record = { s: 0 for s in range(steps)}
grid = MakeGrid(size)
grid = Run(grid, steps)
totals = ProcessRecord(Record, 0)
print(f'{totals = }')
