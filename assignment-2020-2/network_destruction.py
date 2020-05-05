import argparse
import pprint
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--nodesnumber", action="store_true", help="nodes number")
parser.add_argument("-r RADIUS", "--radius", type=int, help="radius")
parser.add_argument("num_nodes", type=int, help="number of nodes to substract")
parser.add_argument("input_file", help="input file")
args = parser.parse_args()

def read_file(file=args.input_file):
    g = {}
    with open(file) as graph_input:
        for line in graph_input:
            nodes = [int(x) for x in line.split()]
            if len(nodes) != 2:
               continue
            if nodes[0] not in g:
                g[nodes[0]] = []
            if nodes[1] not in g:
                g[nodes[1]] = []
            g[nodes[0]].append(nodes[1])
            g[nodes[1]].append(nodes[0])
    return g

def degree(g, num=args.num_nodes):
    for k in range(num):
        max_node = 0
        max_counter = 0
        for node in g:
            counter = 0
            for neighbour in g[node]:
                counter += 1
            if counter > max_counter:
                max_counter = counter
                max_node = node
            elif counter == max_counter:
                if node < max_node:
                    max_node = node
        print(max_node, max_counter)
        g.pop(max_node)
        for node in g:
            if max_node in g[node]:
                g[node].remove(max_node)

def bfs(graph, node, r):
    visited = []
    queue = []

    ball = []
    thetaball = []

    visited.append(node)
    queue.append(node)

    levels = {}
    levels[node] = 0

    while queue:

        s = queue.pop(0)

        for neighbour in graph[s]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
                level = levels[s] + 1
                levels[neighbour] = []
                levels[neighbour] = level

    for node in levels:
        if levels[node] <= r:
            ball.append(node)
        if levels[node] == r:
            thetaball.append(node)
    return ball, thetaball

def collective_influence(g, node, r):
    ball, thetaball = bfs(g, node, r)
    num = int(len(g[node])) - 1
    counter = 0
    for nodetheta in thetaball:
        counter += len(g[nodetheta]) - 1
    final = counter * num
    return node, final

def total_ci(g, r):
    ci = []
    for node in g:
        node, final = collective_influence(g, node, r)
        ci.append([node, final])
    return ci

def find_max_ci(ci):
    max_node = 0
    max_counter = 0
    for node in ci:
        if node[1] > max_counter:
            max_counter = node[1]
            max_node = node [0]
        elif node[1] == max_counter:
            if node[0] < max_node:
                max_node = node[0]
    print(max_node, max_counter)
    return(max_node)

def delete_nodes(g, r, num):
    ci = total_ci(g, r)
    for x in range(num):
        node = find_max_ci(ci)
        ball, thetaball = bfs(g, node, r+1)
        for node1 in g:
            if node in g[node1]:
                g[node1].remove(node)
        g.pop(node)
        ball.remove(node)
        for node4 in ci:
            if node == node4[0]:
                ci.remove(node4)
        for ballnode in ball:
            node2, newci = collective_influence(g, ballnode, r)
            for node3 in ci:
                if node3[0] == node2:
                    node3[1] = newci

g = read_file()

if args.nodesnumber:
    degree(g)
elif args.radius:
    delete_nodes(g, args.radius, args.num_nodes)