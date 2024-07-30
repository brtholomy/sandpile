import click
import copy
import random
import struct
from dataclasses import dataclass
from collections import defaultdict
import math
import pickle

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

def WeightedCoord(grid, weight):
    size = len(grid) - 1
    random.seed()
    if weight:
        sample = list(range(size))
        # weight the center according to a given factor:
        weights = [1*weight / abs(i - size/2) for i in range(size)]
        ch = random.choices(sample, weights=weights, k=2)
        coord = Coord(ch[0], ch[1])
    else:
        coord = RandomCoord(grid)
    return coord

def PlaceGrain(grid, coord):
    grid[coord.x][coord.y] += 1
    return grid

def WillFall(grid, height, coord):
    return grid[coord.x][coord.y] > height

def WithinGrid(grid, coord):
    size = len(grid)
    return coord.x < size and coord.y < size

def GetNeighborsCross(coord):
    return [
        Coord(coord.x + 1, coord.y),
        Coord(coord.x, coord.y + 1),
        Coord(coord.x - 1, coord.y),
        Coord(coord.x, coord.y - 1),
    ]

def GetNeighborsX(coord):
    return [
        Coord(coord.x + 1, coord.y + 1),
        Coord(coord.x - 1, coord.y - 1),
        Coord(coord.x + 1, coord.y - 1),
        Coord(coord.x - 1, coord.y + 1),
    ]

def GetNeighbors(coord, shape='cross'):
    if shape == 'all':
        return GetNeighborsCross(coord) + GetNeighborsX(coord)
    elif shape == 'x':
        return GetNeighborsX(coord)
    else:
        return GetNeighborsCross(coord)

def Cascade(snapshots, record, grid, height, coord, step):
    if WillFall(grid, height, coord):
        grid[coord.x][coord.y] -= 8
        record[step] += 1
        for n in GetNeighbors(coord, 'all'):
            if WithinGrid(grid, n):
                grid = PlaceGrain(grid, n)
                snapshots.append(copy.deepcopy(grid))
                return Cascade(snapshots, record, grid, height, n, step)
    return snapshots, grid

def Run(grid, height, iters, weight):
    snapshots = []
    record = defaultdict(int)
    for step in range(iters):
        coord = WeightedCoord(grid, weight)
        grid = PlaceGrain(grid, coord)
        snapshots, grid = Cascade(snapshots, record, grid, height, coord, step)
        snapshots.append(copy.deepcopy(grid))
    return snapshots, record

def ProcessRecord(rec, threshold):
    totals = defaultdict(int)
    for cascades in rec.values():
        if cascades > threshold:
            totals[cascades] += 1
    # resort it, since defaultdict keeps order, but the smallest cascade isn't
    # guaranteed to come first:
    totals = { k:v for k,v in sorted(totals.items()) }
    return totals

def MapToLog(totals):
    logs = {}
    for cascades, num in totals.items():
        logs[cascades] = math.log(num)
    return logs

def PowerLawEstimation(logs, powlaw):
    curve = {}
    for i in range(len(logs)):
        curve[i] = math.exp(i * powlaw)
    return curve


@click.command()
@click.option(
    '--height', '-h',
    default=4,
    show_default=True,
    help='Maximum height of a given site'
)
@click.option(
    '--size', '-s',
    default=10,
    show_default=True,
    help='Number of sites, M, in the MxM lattice'
)
@click.option(
    '--iters', '-i',
    default=1_000,
    type=int,
    show_default=True,
    help='Number of iterations'
)
@click.option(
    '--counter_threshold', '-c',
    default=0,
    type=int,
    show_default=True,
    help='Threshold above which the cascade counter should apply'
)
@click.option(
    '--video', '-v',
    is_flag=True,
    default=False,
    help='Record a video of the simulation progression'
)
@click.option(
    '--plot_totals', '-t',
    is_flag=True,
    default=False,
    help='Make a plot of the totals'
)
@click.option(
    '--plot_logs', '-l',
    is_flag=True,
    default=False,
    help='Make a plot of the logarithmic reduction'
)
@click.option(
    '--center_weight', '-w',
    default=0,
    type=float,
    show_default=True,
    help='weight the center by the given factor. default is random placement'
)
@click.option(
    '--seed',
    is_flag=True,
    default=False,
    help='Load a previously saved grid as seed'
)
@click.option(
    '--save',
    is_flag=True,
    default=False,
    help='Save the last frame of this run for a seed, as grid.pkl'
)
def main(height, size, iters, counter_threshold, video, plot_totals, plot_logs,
         center_weight, seed, save):
    if seed:
        with open('grid.pkl', 'rb') as f:
            grid = pickle.load(f)
    else:
        grid = MakeGrid(size)

    snapshots, record = Run(grid, height, iters, center_weight)
    totals = ProcessRecord(record, counter_threshold)
    print(f'{totals = }')
    logs = MapToLog(totals)
    print(f'{logs = }')

    if video:
        viz.Video(snapshots, height, fps=15, cmap='Blues', filename='results.mp4')

    if plot_totals:
        viz.PlotTotals(totals)

    if plot_logs:
        viz.PlotTotals(logs, 'line')

    if save:
        with open('grid.pkl', 'wb') as f:
            pickle.dump(grid, f)


if __name__ == "__main__":
    main()
