import argparse
import pprint
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--verbose", action="store_true", help="print")
parser.add_argument("n", type=int, help="size")
args = parser.parse_args()

def create_square_lattice(size):
    square_lattice = []
    square_list = []
    for row in range(size):
        for column in range(size):
            square_lattice.append((row,column))
            if row != 0 and column != 0:
                square_lattice.append((-row, column))
    for square in square_lattice:
        if square[1] > 0:
            square_list.append(square)
        elif square[1] == 0 and square[0] >= 0:
            square_list.append(square)
    return square_list

def create_graph(square_list, n):
    g = {}
    for square in square_list:
        if abs(square[0]) + square[1] < n:
            if square not in g:
                g[square] = []
            for nextsquare in square_list:
                if abs(nextsquare[0]) + nextsquare[1] < n:
                    if square[1] == nextsquare[1] and nextsquare[0] - square[0] == 1:
                        g[square].append(nextsquare)
                    elif square[0] == nextsquare[0] and nextsquare[1] - square[1] == -1:
                        g[square].append(nextsquare)
                    elif square[1] == nextsquare[1] and nextsquare[0] - square[0] == -1:
                        g[square].append(nextsquare)
                    elif square[0] == nextsquare[0] and nextsquare[1] - square[1] == 1:
                        g[square].append(nextsquare)
    return g

def find_neighbors(g, p, u):
    neighbors = []
    for v in p:
        if v == u:
            continue
        else:
            for k in g[v]:
                if k not in p:
                    neighbors.append(k)
    return neighbors

def cfp(g, untried, n, p, c):
    while untried:
        u = untried.pop()
        p.append(u)
        if len(p) == n:
            c+=1
        else:
            new_neighbors = []
            for v in g[u]:
                if v not in untried and v not in p and v not in find_neighbors(g, p, u):
                    new_neighbors.append(v)
            new_untried = untried + new_neighbors
            c=cfp(g, new_untried, n, p, c)
        p.remove(u)
    return c

n = args.n
square_list = create_square_lattice(n)
g = create_graph(square_list, n)
untried = [(0,0)]
p = []
c = 0
c = cfp(g, untried, n, p, c)

if args.verbose:
    pprint.pprint(g)
    print(c)
else:
    print(c)