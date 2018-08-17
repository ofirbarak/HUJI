import os
import sys


def first_pass(filename):
    with open(filename, "r") as text_file:
        global table
        line_number = 0
        for line in text_file:
            end_index = -1
            if line.find("//") == 0 or line.find("\n") == 0:
                continue
            if line.find("//") != -1:
                end_index = line.find("//")
            line = line[:end_index].strip()
            variable = line[1:]
            if line.startswith("@") and not variable.isdigit():
                if variable == "SP":
                    table[variable] = 0
                if variable == "LCL":
                    table[variable] = 1
                if variable == "ARG":
                    table[variable] = 2
                if variable == 'THIS':
                    table[variable] = 3
                if variable == 'THAT':
                    table[variable] = 4
                if variable[0] == 'R':
                    if len(variable) == 2 or len(variable) == 3 and variable[1:].isdigit():
                        table[line[1:]] = variable[1:]
                if variable == "SCREEN":
                    table[line[1:]] = 16384
                if variable == "KBD":
                    table[line[1:]] = 24576
            if line.startswith("(") and line.endswith(")"):
                table[line[1:-1]] = line_number
                line_number -= 1
            line_number += 1



def dest_parsing(dest):
    if dest == "M":
        return ['0', '0', '1']
    if dest == "D":
        return ['0', '1', '0']
    if dest == "MD":
        return ['0', '1', '1']
    if dest == "A":
        return ['1', '0', '0']
    if dest == "AM":
        return ['1', '0', '1']
    if dest == "AD":
        return ['1', '1', '0']
    if dest == "AMD":
        return ['1', '1', '1']
    return ['0', '0', '0']

def jump_parser(jump):
    if jump == "JGT":
        return ['0', '0', '1']
    if jump == "JEQ":
        return ['0', '1', '0']
    if jump == "JGE":
        return ['0', '1', '1']
    if jump == "JLT":
        return ['1', '0', '0']
    if jump == "JNE":
        return ['1', '0', '1']
    if jump == "JLE":
        return ['1', '1', '0']
    if jump == "JMP":
        return ['1', '1', '1']
    return ['0', '0', '0']

def comp_parser(comp):
    if comp == "0":
        return ['1', '0', '1', '0', '1', '0'], '0'
    if comp == "1":
        return ['1', '1', '1', '1', '1', '1'], '0'
    if comp == "-1":
        return ['1', '1', '1', '0', '1', '0'], '0'
    if comp == "D":
        return ['0', '0', '1', '1', '0', '0'], '0'
    if comp == "A" or comp == "M":
        return ['1', '1', '0', '0', '0', '0'], ('0' if comp == 'A' else '1')
    if comp == "!D":
        return ['0', '0', '1', '1', '0', '1'], '0'
    if comp == "!A" or comp == "!M":
        return ['1', '1', '0', '0', '0', '1'], ('0' if comp == '!A' else '1')
    if comp == "-D":
        return ['0', '0', '1', '1', '1', '1'], '0'
    if comp == "-A" or comp == "-M":
        return ['1', '1', '0', '0', '1', '1'], ('0' if comp == '-A' else '1')
    if comp == "D+1":
        return ['0', '1', '1', '1', '1', '1'], '0'
    if comp == "A+1" or comp == "M+1":
        return ['1', '1', '0', '1', '1', '1'], ('0' if comp == 'A+1' else '1')
    if comp == "D-1":
        return ['0', '0', '1', '1', '1', '0'], '0'
    if comp == "A-1" or comp == "M-1":
        return ['1', '1', '0', '0', '1', '0'], ('0' if comp == 'A-1' else '1')
    if comp == "D+A" or comp == "D+M":
        return ['0', '0', '0', '0', '1', '0'], ('0' if comp == 'D+A' else '1')
    if comp == "D-A" or comp == "D-M":
        return ['0', '1', '0', '0', '1', '1'], ('0' if comp == 'D-A' else '1')
    if comp == "A-D" or comp == "M-D":
        return ['0', '0', '0', '1', '1', '1'], ('0' if comp == 'A-D' else '1')
    if comp == "D&A" or comp == "D&M":
        return ['0', '0', '0', '0', '0', '0'], ('0' if comp == 'D&A' else '1')
    if comp == "D|A" or comp == "D|M":
        return ['0', '1', '0', '1', '0', '1'], ('0' if comp == 'D|A' else '1')
    if comp == "D<<":
        return ['1', '1', '0', '0', '0', '0'], '0'
    if comp == "D>>":
        return ['0', '1', '0', '0', '0', '0'], '0'
    if comp == "A<<":
        return ['1', '0', '0', '0', '0', '0'], '0'
    if comp == "A>>":
        return ['0', '0', '0', '0', '0', '0'], '0'
    if comp == "M<<":
        return ['1', '0', '0', '0', '0', '0'], '1'
    if comp == "M>>":
        return ['0', '0', '0', '0', '0', '0'], '1'

def second_pass(filename, outputfile):
    with open(filename, "r") as text_file, open(outputfile, "w") as out_file:
        global table
        first_empty_rom = 16
        for line in text_file:
            if line.startswith("(") and line.endswith(")\n") or line.startswith("//") or line == "\n":
                continue
            end_index = -1
            if line.find("//") != -1:
                end_index = line.find("//")
            line = line[:end_index].strip()
            if line.startswith("@"):
                value = line[1:]
                if not line[1:].isdigit():
                    if line[1:] in table:
                        value = table[line[1:]]
                    else:
                        value = first_empty_rom
                        table[line[1:]] = first_empty_rom
                        first_empty_rom += 1
                bin_value = bin(int(value))[2:]
                while len(bin_value) < 15:
                    bin_value = '0' + bin_value
                out_file.write("0" + str(bin_value) + "\n")

            else:
                equal_index = line.find('=')
                jmp_index = line.find(";")
                comp_bits = ['0', '0', '0', '0', '0', '0']
                dest_bits = ['0', '0', '0']
                jump_bits = ['0', '0', '0']
                a_bit = 0
                if equal_index != -1:
                    dest = line[:equal_index].strip()
                    dest_bits = dest_parsing(dest)
                    comp = line[equal_index + 1:].strip()
                    comp_bits, a_bit = comp_parser(comp)
                if jmp_index != -1:
                    jump = line[jmp_index + 1:].strip()
                    jump_bits = jump_parser(jump)
                    comp = line[equal_index + 1:jmp_index].strip()
                    comp_bits, a_bit = comp_parser(comp)
                if line.find("<<") != -1 or line.find(">>") != -1:
                    out_file.write("101" + str(a_bit) + ''.join(comp_bits) +
                               ''.join(dest_bits) + ''.join(jump_bits)+"\n")
                else:
                    out_file.write("111" + str(a_bit) + ''.join(comp_bits) +
                               ''.join(dest_bits) + ''.join(jump_bits)+"\n")


table = dict()
filename = sys.argv[1]
if os.path.isdir(filename):
    for file in os.listdir(filename):
        if not file.endswith(".asm") or os.path.isdir(file):
            continue
        outputfile = os.path.join(filename, file[:file.index('.')] + ".hack")
        first_pass(os.path.join(filename, file))
        second_pass(os.path.join(filename, file), outputfile)
if filename.endswith(".asm"):
    outputfile = filename[:filename.index('.')]+".hack"
    first_pass(filename)
    second_pass(filename, outputfile)