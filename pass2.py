# this program is a pass2 in sic hypothetical machine
# Dalia etemaiza

def file_reading(file):
    """read intermediate  file.
    :param file: file name that contain intermediate
    :return: 2D array in form [[location,label,instruction or directive,operand],........]
    """

    inputFile = open(file, "rt")
    dataFile = []
    for line in inputFile:
        # split line to location , label , instruction ,data and store in 2d array
        col = [line[0:9].strip(), line[10:26].strip(), line[27:43].strip(), line[44:60].strip()]
        dataFile.append(col)

    inputFile.close()
    return dataFile


def tab_read(file):
    """read file and store data in hash table(direction in python).
    :return : optable and symtab in hash table( dictionary in python).
    """

    _tabel = {}
    inputFile = open(file, "rt")
    for line in inputFile:
        _tabel[line[0:10].strip()] = line[11:15].strip()
    inputFile.close()
    return _tabel


def write_file(item, out, object):
    """write in the listing file
       :param item:array [location ,label ,instruction and operand] from intermediate file.
       :param out : file (list file) to write in.
       :param object : string -> object code for line.
       """
    for i in item:
        blanks = 15 - len(i)
        out.write(i + " " * blanks)

    out.write(object + "\n")


def text_record(list, out, add):
    """write text record in the object file
           :param list:array contain objects code in text record
           :param out : file (object file) to write in.
           :param add : address for text record
           """
    length = hex(len(list) * 3)[2:]
    for i in list:
        if len(i) > 6:
            length = hex(int(length, 16) + int((6 - len(i)) / 2))[2:]
        elif len(i) < 6:
            length = hex(int(length, 16) - int((6 - len(i)) / 2))[2:]
    out.write('T^' + add + '^' + length)
    for i in list:
        out.write('^' + i)

    out.write('\n')


def pass_2(intermediate, obtab, symtab):
    """write in the listing file
           :param intermediate:array [location ,label ,instruction and operand] from intermediate file.
           :param obtab : dictionary for instruction and there obcode.
           :param symtab : dictionary for symbol and there location in program.
           :return error_list: list contain errors in program.
           """
    error_array = []  # array for error in code
    text_array = []  # array for text records
    object_code = ''
    # open files(listing + symbol)
    list = open("listing.lst", "w")
    object1 = open("object.obj", "w")
    directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW"]
    length = hex(int(int(intermediate[len(intermediate) - 1][0], 16) - int(intermediate[0][3], 16)))[2:]
    if intermediate[0][2] != "START":  # handel error in  first line
        print("\033[1;31m"+"you have an error in pass one")
        return 0
    elif intermediate[len(intermediate) - 1][2] != "END":  # handel error in last line
        print("\033[1;31m"+"you have an error in pass one")
        return 0
    else:
        text_address = intermediate[0][0]  # first location for text record
        for item in intermediate:
            if (len(text_array) > 9 or (item[2] == 'RESW') or (item[2] == 'RESB') or item[2] == 'END') and len(
                    text_array) > 0:  # (if text record have more than 9 instruction or address not continues print
                # text record).
                text_record(text_array, object1, text_address)
                text_array = []  # clear array after print text record.
                text_address = item[0]  # clear address
            if item[2] == 'START':
                object1.write("H^" + item[1] + "^" + item[3] + "^" + length + '\n')  # print header record.
                object_code = ""
            elif item[2] == 'END':
                object1.write("E^" + symtab[item[3]] + '\n')
                object_code = ""
                write_file(item, list, object_code)
                return error_array
            elif item[2] == 'RSUB':
                object_code = obtab[item[2]] + "0000"
            elif item[2] in obtab.keys():
                if ',X' in item[3]:
                    if (item[3].replace(',X', "")) in symtab.keys():
                        operand = symtab[item[3].replace(',X', "")]
                        object_code = obtab[item[2]] + hex(int(operand[0], 16) + 8)[2:] + operand[1:]

                    else:
                        error_array.append("undefined symbol in line" + item[0])
                        object_code = obtab[item[2]] + "0000"

                else:
                    if item[3] in symtab:
                        object_code = obtab[item[2]] + symtab[item[3]]

                    else:
                        error_array.append("undefined symbol in line" + item[0])
                        object_code = obtab[item[2]] + "0000"

            elif item[2] in directives:
                if item[2] == 'WORD':
                    if item[3][0] == "-":
                        item[3] = item[3][1:]
                        if item[3].isdigit():
                            value = hex(((int(item[3]) * -1) + (1 << 24)) % (1 << 24))[2:]
                            item[3] = "-" + item[3]
                            object_code = ('0' * (6 - len(value))) + value
                    elif item[3].isdigit():
                        value = hex(int(item[3]))[2:]
                        object_code = ('0' * (6 - len(value))) + value
                    else:
                        error_array.append("error in " + item[2] + " you cant using word with string it should be "
                                                                   "integer!!!")

                elif item[2] == 'BYTE':
                    if item[3][0] == 'X':
                        object_code = item[3][2:-1]
                    elif item[3][0] == 'C':
                        object_code = item[3][2:-1].encode("utf-8").hex()

                else:
                    if item[3].isdigit():
                        object_code = ""
                        if item[2] == 'RESW':
                            text_address = hex(int(text_address, 16) + (int(item[3]) * 3))[2:]

                        else:
                            text_address = hex(int(text_address, 16) + (int(item[3])))[2:]

                    else:
                        error_array.append("error in " + item[2] + " you cant reserve a string value!!!")
            else:
                error_array.append("undefined instruction in line" + item[0])

            write_file(item, list, object_code)
            if object_code != '':
                text_array.append(object_code)


if __name__ == '__main__':
    intermediate = file_reading("intermediate.mdt")
    optable = tab_read('opt.txt')
    symtable = tab_read('symbol.txt')
    error_list = pass_2(intermediate, optable, symtable)

    if error_list:  # check if sic program contain errors or not.
        print("ERROR LIST")
        for i in error_list:
            print("\033[1;31m" + i)  # print error in red color

    elif error_list==0:
        pass
    else:
        print("\033[1;32m no error")  # print no error in green color
