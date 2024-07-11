import copy
import random
import struct
from dataclasses import dataclass
from collections import defaultdict
import math

import visualization as viz

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

def CenterWeightedCoord(grid):
    size = len(grid) - 1
    random.seed()
    sample = list(range(size))
    # weight the center
    weights = [1 / abs(i - size/2) for i in range(size)]
    ch = random.choices(sample, weights=weights, k=2)
    return Coord(ch[0], ch[1])

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

def GetNeighbors8(coord):
    return [
        Coord(coord.x + 1, coord.y),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x + 1, coord.y + 1),
        Coord(coord.x - 1, coord.y),
        Coord(coord.x, coord.y - 1),
        Coord(coord.x - 1, coord.y - 1),
        Coord(coord.x + 1, coord.y - 1),
        Coord(coord.x - 1, coord.y + 1),
    ]

def Cascade(snapshots, grid, coord, step):
    if WillFall(grid, coord):
        grid[coord.x][coord.y] -= 8
        Record[step] += 1
        for n in GetNeighbors(coord):
            if WithinGrid(grid, n):
                grid = PlaceGrain(grid, n)
                snapshots.append(copy.deepcopy(grid))
                return Cascade(snapshots, grid, n, step)
    return snapshots, grid

def Run(grid, steps):
    snapshots = []
    for step in range(steps):
        coord = CenterWeightedCoord(grid)
        grid = PlaceGrain(grid, coord)
        snapshots, grid = Cascade(snapshots, grid, coord, step)
        snapshots.append(copy.deepcopy(grid))
    return snapshots

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

MAXHEIGHT = 8
size = 10
steps = 1000
counter_threshold = 0

Record = { s: 0 for s in range(steps)}
grid = MakeGrid(size)
snapshots = Run(grid, steps)
totals = ProcessRecord(Record, counter_threshold)
print(f'{totals = }')
logs = MapToLog(totals)
print(f'{logs = }')
print(f'{PowerLawEstimation(logs, 1/3) = }')

viz.Video(snapshots, MAXHEIGHT, fps=15, cmap='Blues', filename='results.mp4')
