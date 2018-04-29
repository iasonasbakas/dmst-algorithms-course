import argparse
import pprint
import csv
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="<input_file>")
args = parser.parse_args()

def read_file(filename=args.filename):
    square = []
    with open(filename, newline='') as file:
        rows = csv.reader(file, skipinitialspace=True)
        for row in rows:
            if len(row) == 0:
                continue
            else:
                square.append(row)
    return square

def dfs(square, number, row, collumn):
    transversal.append(number)
    visited.append(row)
    if len(transversal) == length:
        transversal1 = transversal[:]
        transversals.append(transversal1)
    else:
        for v in range(length):
            if v not in visited:
                if square[v][collumn+1] not in transversal and collumn+1<length:
                    number = square[v][collumn+1]
                    dfs(square, number, v, collumn+1)
                elif not collumn+1<length:
                    transversal.append(number)
    transversal.pop()
    visited.pop()

def find_all_transversals():
    for v in range(length):
        number = square[v][0]
        dfs(square, number, v, 0)

def create_dictionary():
    dict_transversals = {}
    for num in range(length):
        dict_transversals[num] = []
        for transversal in transversals:
            transversal1 = int(transversal[0])
            if transversal1 == num:
                dict_transversals[num].append(transversal)
    return dict_transversals

def are_equals(trans, final):
    equal = False
    for i, j in zip(trans, final_transversals[final]):
        if i == j:
            equal = True
    return equal

def dfs_correct_transversals(transversal, row):
    final_transversals.append(transversal)
    if len(final_transversals) == length:
        final_transversals2 = final_transversals[:]
        ultra_final_transversals.extend(final_transversals2)
        found = True
        return found
    else:
        for tran in dict_transversals[row+1]:
            is_different = True
            for rowf in range(len(final_transversals)):
                if are_equals(tran,rowf):
                    is_different = False
            if is_different:
                dfs_correct_transversals(tran, row+1)
    final_transversals.pop()

def find_correct_transversals():
    i=0
    while (i<len(dict_transversals[0])) and not found:
        dfs_correct_transversals(dict_transversals[0][i], 0)
        i += 1

def create_latin_square():
    for tran in ultra_final_transversals:
        number = tran[0]
        for collumn in range(length):
            for row in range(length):
                if square[row][collumn] == tran[collumn]:
                    latin_square[row][collumn] = number

def create_gr_la_square():
    if latin_square:
        for i in range(length):
            row = list(zip(square[i], latin_square[i]))
            gr_la_square.append(row)



square = read_file()
length = len(square[0])
transversal = []
visited = []
transversals = []
found = False
final_transversals = []
ultra_final_transversals = []
find_all_transversals()
transversals.sort()
dict_transversals = create_dictionary()
find_correct_transversals()
latin_square = []
if transversals:
    latin_square = deepcopy(square)
create_latin_square()
gr_la_square = []
create_gr_la_square()
pprint.pprint(gr_la_square)
