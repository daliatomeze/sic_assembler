# this program is a pass1 in sic hypothetical machine
# Dalia etemaiza


import os
from array import *
from texttable import Texttable
from prettytable import PrettyTable


def file_reading(file):
    """read SIC program file.
    :param file: file name that contain sic program
    :return: 2D array in form [[label,instruction or directive,opreand],........]
    """

    inputFile = open(file, "rt")
    dataFile = []
    for line in inputFile:
        if line[0] == ".":  # skip comment line
            continue
        # split line to label , instruction ,data and store in 2d array
        col = [line[0:10].strip(), line[12:20].strip(), line[22:39].strip()]
        dataFile.append(col)

    inputFile.close()
    return dataFile


def optab_read():
    """" read instruction and opcode and store them in hash table(direction in python).
    :return : optable in hash table( dictionary in python).
    """

    op_tabel = {}
    inputFile = open('opt.txt', "rt")
    for line in inputFile:
        op_tabel[line[0:10].strip()] = line[11:13].strip()
    inputFile.close()
    return op_tabel


def locctr(data, optab):
    """" pass1 assembler write in intermediate file as location,label,inst or directive ,operand.
    :parameter data : sic program that store in 2d array
    :parameter optab: opcode table in dictionary
    :return : Symbol table as dictionary
    """

    out = open("intermediate.mdt", "w")
    symtab = {}
    directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]
    if data[0][1] != "START":  # handel error in  first line
        print("you have an error in first line : where Start !!")
        return 0
    elif data[len(data) - 1][1] != "END":  # handel error in last line
        print("you have an error in last line : where END !!")
        return 0
    else:
        print("\nProgram Name   :" + data[0][0])
        print("Program Location   :" + data[0][2])
        first_location = data[0][2]
        Locctr = '0x' + data[0][2]
        for item in data:
            if item[0] != '':  # check if line contain label to add to symbol table.
                if item[1] != "START":
                    if item[0] in symtab.keys():
                        print('ERROR : duplicat Symbol ==> ' + item[0])
                        return 0
                    symtab[item[0]] = Locctr[2:]
            inst = item[1]
            if inst in directives:
                blanks = 10 - len(Locctr[2:])  # write in intermediate file
                out.write(Locctr[2:] + " " * blanks)
                for i in item:
                    blanks = 17 - len(i)
                    out.write(i + " " * blanks)
                out.write("\n")

                if inst == 'WORD':
                    Locctr = hex(int(Locctr[2:], 16) + 3)
                elif inst == 'RESW':
                    count = item[2]
                    Locctr = hex(int(Locctr[2:], 16) + (int(count) * 3))
                elif inst == 'RESB':
                    count = item[2]
                    Locctr = hex(int(Locctr[2:], 16) + (int(count)))
                elif inst == 'BYTE':
                    if item[2][0] == 'X':
                        Locctr = hex(int(Locctr[2:], 16) + int((len(item[2]) - 2) / 2))

                    elif item[2][0] == 'C':
                        Locctr = hex(int(Locctr[2:], 16) + (len(item[2]) - 3))
                    else:
                        print("invalid oprend in line "+Locctr)
                        return 0;
                elif inst == 'END':
                    print("Program Length   :" + hex(int(int(Locctr[2:], 16) - int(first_location,16)))[2:])

            elif inst in optab.keys():
                blanks = 10 - len(Locctr[2:])
                out.write(Locctr[2:] + " " * blanks)
                for i in item:
                    blanks = 17 - len(i)  # maximum operand length
                    out.write(i + " " * blanks)
                out.write("\n")
                Locctr = hex(int(Locctr[2:], 16) + 3)
            else:
                print("error this instruction is not valid!")
                return 0

        return symtab


if __name__ == '__main__':
    data = file_reading("SICFile.txt")
    symbol = open("symbol.txt", "w")
    optab = optab_read()
    tableList = []
    SymTab = locctr(data, optab)
    if SymTab == 0:  # check errors
        pass
    else:
        for i in range(len(SymTab)):
            col = [list(SymTab.items())[i][0], list(SymTab.items())[i][1]]
            tableList.append(col)




        table = PrettyTable(['Symbol', 'Address'])  # using prettyTable library to arrange symbol table.
        for rec in tableList:
            table.add_row(rec)
            blanks = 11 - len(rec[0])
            symbol.write(rec[0] + " " * blanks + rec[1] + '\n')

        print("\nSYMBOL TABLE  :\n")
        print(table)

        symbol.close()
