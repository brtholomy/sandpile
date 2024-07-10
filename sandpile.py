import random
import struct
from dataclasses import dataclass
from collections import defaultdict
import math

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
    return grid[coord.x][coord.y] > MAXHEIGHT

def WithinGrid(grid, coord):
    size = len(grid)
    return coord.x < size and coord.y < size

def GetNeighbors(coord):
    return [
        Coord(coord.x + 1, coord.y),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x - 1, coord.y),
        Coord(coord.x, coord.y - 1),
    ]

def Cascade(grid, coord, step):
    if WillFall(grid, coord):
        grid[coord.x][coord.y] -= 4
        Record[step] += 1
        for n in GetNeighbors(coord):
            if WithinGrid(grid, n):
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
    for step, cascades in rec.items():
        if cascades > threshold:
            totals[cascades] += 1
    return totals

def MapToLog(totals):
    logs = {}
    for cascades, num in totals.items():
        logs[math.log(cascades)] = math.log(num)
    return logs

def PowerLawEstimation(logs, powlaw):
    curve = []
    for i in range(len(logs)):
        curve.append(math.exp(i * powlaw))
    return curve

MAXHEIGHT = 4
size = 20
steps = 10000
counter_threshold = 0

Record = { s: 0 for s in range(steps)}
grid = MakeGrid(size)
grid = Run(grid, steps)
totals = ProcessRecord(Record, counter_threshold)
print(f'{totals = }')
logs = MapToLog(totals)
print(f'{logs = }')
print(f'{PowerLawEstimation(logs, 1/3) = }')
