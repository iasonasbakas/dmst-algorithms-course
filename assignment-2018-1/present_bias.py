import argparse
import pprint
import sys

MAX_INT = sys.maxsize

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="<input_file>")
parser.add_argument("b", help="<bias_parameter>", type=float)
parser.add_argument("start", help="<start_node>")
parser.add_argument("end", help="<end_node>")
args = parser.parse_args()

def read_file(filename=args.filename):
    g = {}
    w = {}
    with open(filename) as graph_input:
        for line in graph_input:
            nodes = [x for x in line.split()]
            if len(nodes) != 3:
                continue
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            nodes[2] = int(nodes[2])
            w[(nodes[0],nodes[1])] = nodes[2]
            g[nodes[0]].append(nodes[1])
    return (g, w)

def dfs(g, start, end, path, paths):
    path.append(start)
    if start == end:
        path1 = path[:]
        paths.append(path1)
    else:
        for v in g[start]:
            dfs(g, v, end, path, paths)
    path.pop()

def best_path(paths, w):
    best = []
    min = MAX_INT
    for path in paths:
        counter = 0
        for i in range(len(path)-1):
            counter += w[path[i],path[i+1]]
        if min>counter:
            min = counter
            best = path
    print(best, min)

def count_path(path, w):
    counter = 0
    for i in range(len(path)-1):
        counter += w[path[i],path[i+1]]
    return counter

def count_biased_path(path, start, end, w, b=args.b):
    if start == end:
        return 0
    else:
        index = path.index(start)
        v = index + 1
        counter = w[start,path[v]]
        if path[-2] == start:
            return counter
        else:
            while start != end:
                counter += b * w[path[v],path[v+1]]
                start = path[v]
                v += 1
                if path[v] == end:
                    break
    return counter

def biased_path(paths, start, end, w, b):
    biased = []
    biased.append(start)
    node = start
    while end not in biased:
        counter = 0
        min = MAX_INT
        for path in paths:
            if node in path:
                counter = count_biased_path(path, node, end, w, b)
                if min>counter:
                    min = counter
                    pathb = path
        if node != end:
            index = pathb.index(node)
            biased.append(pathb[index+1])
            node = pathb[index+1]
        else:
            biased.append(end)
    real = count_path(biased, w)
    print(biased, real)

g, w = read_file()
path = []
paths = []
dfs(g, args.start, args.end, path ,paths)
best_path(paths,w)
biased_path(paths, args.start, args.end, w, args.b)
