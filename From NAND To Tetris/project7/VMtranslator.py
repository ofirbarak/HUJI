import os
import re
import sys


def jump_R14_address():
    """
    Jump to the address in R14
    :return: a string
    """
    return '@R14\n' + \
           'A=M\n' + \
           '0;JMP\n'


def create_end_loop():
    return '(END)\n' + '@END\n' + '0;JMP\n'


def create_make_true_false_label():
    """
    Make labels 'push true', 'push false' and return to the address in R14
    :return:
    """
    str = ''
    str += '(PUSH_TRUE)\n' + \
           'D=-1\n'
    str += push()
    str += jump_R14_address()
    str += '(PUSH_FALSE)\n' + \
           'D=0\n'
    str += push()
    str += jump_R14_address()
    return str


def push():
    """
    pushes the value of D to stack
    :return a string
    """
    output_str = ''
    output_str += "@SP\n"
    output_str += "A=M\n"
    output_str += "M=D\n"
    output_str += "@SP\n"
    output_str += "M=M+1\n"
    return output_str


def pop():
    """
    pop from stack and puts the value in D
    :return a string
    """
    output_str = ''
    output_str += "@SP\n"
    output_str += "M=M-1\n"
    output_str += "A=M\n"
    output_str += "D=M\n"
    return output_str


def peek_last():
    output_str = ''
    output_str += "@SP\n"
    output_str += "A=M-1\n"
    output_str += "D=M\n"
    return output_str


def peek_second_last():
    output_str = ''
    output_str += "@SP\n"
    output_str += "A=M-1\n"
    output_str += "A=A-1\n"
    output_str += "D=M\n"
    return output_str


def copy_last_2_values():
    """
    copy last 2 values in stack to r12=RAM[SP-1],r13=RAM[SP-2]
    """
    return (peek_last() +
            '@R13\n' +
            'M=D\n' +
            peek_second_last() +
            '@R14\n' +
            'M=D\n')


def checkIf(if_op, command):
    """
    Assume:
        x = RAM[SP-2]
        y = RAM[SP-1]
    Check:
        x <(=) y -> D=1 then jump to continue[i]
        x = y -> D=0 then jump to continue[i]
        x >(=) y -> D=-1 then jump to continue[i]
    :return: string representation
    """
    # if y >= 0
    return (copy_last_2_values() +
            '@R13\n' +
            'M=M>>\n' +
            'D=M\n'
            'D=D<<\n' +
            '@R15\n' +
            'M=D\n' +
            peek_last() +
            '@R15\n' +
            'M=D-M\n'
            '@R14\n' +
            'M=M>>\n' +
            'D=M\n'
            'D=D<<\n' +
            '@SP\n' +
            'A=M\n'+
            'A=A-1\n'+
            'A=A-1\n'+
            'D=M-D\n'+
            push()+
            
            '@R13\n' +
            'D=M\n' +
            '@R14\n' +
            'D=M-D\n' +
            '@pushSomething%d\n' % (i + 2) +
            'D;JNE\n' +

            peek_last()+
            '@R15\n' +
            'D=D-M\n' +
            '@pushSomething%d\n' % (i + 2) +
            '0;JMP\n' +

            '(pushSomething%d)\n' % (i + 2) +
            '@SP\n'+
            'M=M-1\n'+
            'M=M-1\n'+
            'M=M-1\n'+
            '@continue%d\n' % (i + 1) +
            '0;JMP\n')


def command_func(command, output_file):
    binary_op = {'add': '+', 'sub': '-', 'and': '&', 'or': '|'}
    if_op = {'eq': 'EQ', 'gt': 'GT', 'lt': 'LT'}
    if command in binary_op:
        output_file.write(pop() +
                          "@SP\n" +
                          "M=M-1\n" +
                          "A=M\n" +
                          "D=M%cD\n" % binary_op[command] +
                          push())
    elif command == 'neg':
        output_file.write('@0\n' +
                          'D=A\n' +
                          '@SP\n' +
                          'M=M-1\n' +
                          'A=M\n' +
                          'D=D-M\n' +
                          push())
    elif command == 'not':
        output_file.write(pop() +
                          "D=!D\n" +
                          push())
    elif command in if_op:
        # create label continue and puts in R14 the address to that label
        global i
        
        output_file.write(checkIf(if_op, command))
        output_file.write('(continue%d)\n' % (i + 1))
        output_file.write(push())
        output_file.write('@continue%d\n' % i)
        output_file.write('D=A\n')
        output_file.write('@R14\n' +
                          'M=D\n')
        output_file.write(pop())
        output_file.write('@PUSH_TRUE\n' +
                          'D;J%s\n' % if_op[command] +
                          '@PUSH_FALSE\n' +
                          '0;JMP\n')
        output_file.write('(continue%d)\n' % i)  # make label for continue
        i += 3


def command_arg1_arg2(command, arg1, arg2, output_file):
    memory_access_op = ['push', 'pop']
    if command in memory_access_op:
        arg_local_helper = {'argument': 'ARG', 'local': 'LCL', 'this': 'THIS', 'that': 'THAT'}
        # this_that_helper = {}
        if command == 'push':
            # D = segment[index]
            if arg1 == 'constant':
                output_file.write('@%s\n' % str(arg2) +
                                  'D=A\n')
            if arg1 in arg_local_helper:
                output_file.write('@%s\n' % arg_local_helper[arg1] +
                                  'D=M\n' +
                                  '@%d\n' % int(arg2) +
                                  'A=D+A\n' +
                                  'D=M\n')
            # elif arg1 in this_that_helper:
            #     output_file.write('@%s\n' % this_that_helper[arg1] +
            #                       'D=M\n')
            if arg1 == 'temp':
                output_file.write('@%d\n' % (int(arg2) + 5) +
                                  'D=M\n')
            if arg1 == 'pointer':
                arg_to_push = 'THIS' if arg2 == '0' else 'THAT'
                output_file.write('@%s\n' % arg_to_push +
                                  'D=M\n')
            if arg1 == 'static':
                output_file.write('@static.%d\n' % (16 + int(arg2)) +  # 16 is base address of static variables
                                  'D=M\n')
            output_file.write(push())  # push d value
        elif command == 'pop':
            output_file.write(pop())
            if arg1 == 'constant':
                output_file.write('@%d\n' % arg2 +
                                  'M=D\n')
            elif arg1 in arg_local_helper:
                output_file.write('@R15\n' +
                                  'M=D\n' +
                                  '@%d\n' % int(arg2) +
                                  'D=A\n' +
                                  '@%s\n' % arg_local_helper[arg1] +
                                  'D=D+M\n' +
                                  '@R14\n' +
                                  'M=D\n'
                                  '@R15\n' +
                                  'D=M\n' +
                                  '@R14\n' +
                                  'A=M\n' +
                                  'M=D\n')
            # elif arg1 in this_that_helper:
            #     output_file.write('@%s\n' % this_that_helper[arg1] +
            #                       'M=D\n')
            elif arg1 == 'temp':
                output_file.write('@%d\n' % (int(arg2) + 5) +
                                  'M=D\n')
            elif arg1 == 'pointer':
                arg_to_pop = 'THIS' if arg2 == '0' else 'THAT'
                output_file.write('@%s\n' % arg_to_pop +
                                  'M=D\n')
            elif arg1 == 'static':
                output_file.write('@static.%d\n' % (16 + int(arg2)) +  # 16 is base address of static variables
                                  'M=D\n')


def parse_file(filename, output_file):
    with open(filename, 'r') as text_file:
        for line in text_file:
            if re.match("^//.+|\s*\n+$", line):
                continue
            cmt_index = line.find('//')
            if cmt_index != -1:
                line = line[:cmt_index]
            line = line.strip()
            result = re.match("^\s*([a-zA-Z]+)\s+(\w+)\s+(\w+)(\s//.)*$", line)
            if result:
                command_arg1_arg2(result.group(1), result.group(2), result.group(3), output_file)
            # result = re.match("(%s)+\s+(%s)+(\s//.)*", line)
            # if result:
            #     command_arg1(result.group(1), result.group(2))
            result = re.match("^([a-zA-Z]+)(\s//.)*$", line)
            if result:
                command_func(result.group(1), output_file)
        


i = 1
filename = sys.argv[1]
end_string = create_end_loop() + create_make_true_false_label()
if os.path.isdir(filename):
    name_final_file = filename[filename.rfind('/')+1:]
    outputfile = os.path.join(filename, name_final_file + ".asm")
    with open(outputfile, 'w') as output_file:
        for file in os.listdir(filename):
            if not file.endswith(".vm") or os.path.isdir(file):
                continue
            parse_file(os.path.join(filename, file), output_file)
        output_file.write(end_string)
if filename.endswith(".vm"):
    outputfile = filename[:filename.index('.')] + ".asm"
    with open(outputfile, 'w') as output_file:
        parse_file(filename, output_file)
        output_file.write(end_string)
