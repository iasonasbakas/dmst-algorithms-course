'''Gnwrizw oti to programma einai asxima grammeno.
Logw loipwn ergasiwn den edwsa emfasi se afto to kommati
kai prospathisa apla na epistrefei to zitoumeno apotelesma.
Iason Bakas'''

import argparse
import pprint
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("values", help="<list of values>", type=int, nargs="+")
args = parser.parse_args()

def binary_convert():
    for num in numbers:
        bin = format(num,'04b')
        binary.append(bin)

def create_table():
    for bin in binary:
        for row in range(4):
            for col in range(4):
                if bin == listABCD[row][col]:
                    bin_list[row][col] = 1
    for row in range(4):
        for col in range(4):
            if bin_list[row][col] != 1:
                bin_list[row][col] = 0

def find_16_size():
    for row in range(4):
        for collumn in range(4):
            if bin_list[row][collumn] != 0:
                return False
    return True

def find_8_size():
    for row in range(4):
        if bin_list[row].count(1) == 4:
            row_8.append(row)
    for collumn in range(4):
        counter = 0
        for row in range(4):
            if bin_list[row][collumn] == 1:
                counter += 1
        if counter == 4:
            collumn_8.append(collumn)
    if len(row_8) + len(collumn_8) > 1:
        for i in row_8:
            for j in range(4):
                row_8_final.append(listABCD[i][j])
        for k in collumn_8:
            for l in range(4):
                collumn_8_final.append(listABCD[l][k])
    if len(row_8_final) != 0:
        final_8.extend(row_8_final)
        final.append(row_8_final)
    if len(collumn_8_final) !=0 :
        final_8.extend(collumn_8_final)
        final.append(collumn_8_final)


def find_4_size():
    for row in range(4):
        for collumn in range(4):
            if row<3:
                if collumn<3:
                    if bin_list[row][collumn] == 1 and bin_list[row][collumn+1]==1 and bin_list[row+1][collumn] == 1 and bin_list[row+1][collumn+1] == 1:
                        epikalipsi = False
                        if listABCD[row][collumn] in final_8:
                            if listABCD[row][collumn+1] in final_8:
                                if listABCD[row+1][collumn] in final_8:
                                    if listABCD[row+1][collumn+1] in final_8:
                                        epikalipsi = True
                        if not epikalipsi:
                            list_4.append(listABCD[row][collumn])
                            list_4.append(listABCD[row][collumn+1])
                            list_4.append(listABCD[row+1][collumn])
                            list_4.append(listABCD[row+1][collumn+1])
                else:
                    if bin_list[row][collumn] == 1 and bin_list[row][0]==1:
                        if listABCD[row][collumn] not in final_8 and listABCD[row][0] not in final_8:
                            list_4.append(listABCD[row][collumn])
                            list_4.append(listABCD[row][0])
            else:
                if collumn<3:
                    if bin_list[row][collumn] == 1 and bin_list[row][collumn+1]==1 and bin_list[0][collumn] == 1 and bin_list[0][collumn+1] == 1:
                        if listABCD[row][collumn] not in final_8:
                            if listABCD[row][collumn+1] not in final_8:
                                if listABCD[0][collumn] not in final_8:
                                    if listABCD[0][collumn+1] not in final_8:
                                        epikalipsi = True
                            list_4.append(listABCD[row][collumn])
                            list_4.append(listABCD[row][collumn+1])
                            list_4.append(listABCD[0][collumn])
                            list_4.append(listABCD[0][collumn+1])
                else:
                    if bin_list[row][collumn] == 1 and bin_list[row][0]==1:
                        if listABCD[row,collumn] not in final_8 and listABCD[row][0] not in final_8:
                            list_4.append(listABCD[row][collumn])
                            list_4.append(listABCD[row][0])
        final_4.extend(list_4)
        if len(list_4) == 4:
            final2 = deepcopy(list_4)
            final.append(final2)
            list_4.clear()

def find_2_size():
    for row in range(4):
        for collumn in range(4):
            if collumn<3:
                if bin_list[row][collumn] == 1 and bin_list[row][collumn+1]==1:
                    if listABCD[row][collumn] not in final_4 and listABCD[row][collumn+1] not in final_4:
                        list_2.append(listABCD[row][collumn])
                        list_2.append(listABCD[row][collumn+1])
            else:
                if bin_list[row][collumn] == 1 and bin_list[row][0]==1:
                    if listABCD[row][collumn] not in final_4 and listABCD[row][0] not in final_4:
                        list_2.append(listABCD[row][collumn])
                        list_2.append(listABCD[row][0])
    for collumn in range(4):
        for row in range(4):
            if row<3:
                if bin_list[row][collumn] == 1 and bin_list[row+1][collumn]==1:
                    if listABCD[row][collumn] not in final_4 and listABCD[row+1][collumn] not in final_4:
                        list_2.append(listABCD[row][collumn])
                        list_2.append(listABCD[row+1][collumn])
            else:
                if bin_list[row][collumn] == 1 and bin_list[0][collumn]==1:
                    if listABCD[row][collumn] not in final_4 and listABCD[0][collumn] not in final_4:
                        list_2.append(listABCD[row][collumn])
                        list_2.append(listABCD[0][collumn])
        final_2.extend(list_2)
        if len(list_2) == 2:
            final2 = deepcopy(list_2)
            final.append(final2)
            list_2.clear()

def find_1_size():
    for row in range(4):
        for collumn in range(4):
            if bin_list[row][collumn] == 1 :
                if listABCD[row][collumn] not in final_2 and listABCD[row][collumn] not in final_4 and listABCD[row][collumn] not in final_8:
                    final.append([listABCD[row][collumn]])

def create_minterms():
    if sixteen:
        print('F=1')
    else:
        count = 0
        for team in final:
            minterm = ''
            if len(team) == 8:
                count += 1
            elif len(team) == 4:
                count += 2
            elif len(team) == 2:
                count += 3
            elif len(team) == 1:
                count += 4
            for col in range(4):
                is_One = True
                is_Zero = True
                for row in range(len(team)):
                    if team[row][col] == '1':
                        is_Zero = False
                    elif team[row][col] == '0':
                        is_One = False
                if col == 0:
                    if is_Zero:
                        minterm += '~A'
                    if is_One:
                        minterm += 'A'
                elif col == 1:
                    if is_Zero:
                        minterm += '~B'
                    if is_One:
                        minterm += 'B'
                elif col == 2:
                    if is_Zero:
                        minterm += '~C'
                    if is_One:
                        minterm += 'C'
                else:
                    if is_Zero:
                        minterm += '~D'
                    if is_One:
                        minterm += 'D'
            minterms.append(minterm)
        minterms.sort()
        finmin = ""
        for min in minterms:
            finmin += min + ' \u2228 '
        finmin = finmin[:-2]
        print(finmin,count)

numbers = args.values
listABCD = [['0000', '0100', '1100', '1000'],
            ['0001', '0101', '1101', '1001'],
            ['0011', '0111', '1111', '1011'],
            ['0010', '0110', '1110', '1010']]
binary = []
bin_list = deepcopy(listABCD)
row_8 = []
row_8_final = []
collumn_8 = []
collumn_8_final = []
final_8 = []
final_4 = []
list_4 = []
final_2 = []
list_2 = []
final_1 = []
final = []
minterms = []
binary_convert()
create_table()
sixteen = find_16_size()
find_8_size()
find_4_size()
find_2_size()
find_1_size()
create_minterms()
