import writer
import sys
import os

keyword_list = ['class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void',
                'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']
symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
               '-', '*', '/', '&', '|', '<', '>', '=', '~']
special_symbol = ['<=', '>=', '!=', '++', '--']
operations = {'+': 'add', '-': 'sub', '*': 'multiply', '/': 'divide', '|': 'or', '&': 'and', '<': 'lt', '=': 'eq',
              '>': 'gt'}


class parser:
    def __init__(self, outputfile, tokens):
        self.__writer = writer.Writer(outputfile)
        self.__lut = {'static': [0], 'field': [0], 'labels': [0]}
        self.__name = tokens[1]

    def compile_class(self):
        global token_idx
        token_idx = 3
        while tokens[token_idx] in ['static', 'field']:
            self.class_variables()
        while tokens[token_idx] in ['constructor', 'function', 'method']:
            self.function_writer()

    def function_writer(self):
        global token_idx
        func_type = token = tokens[token_idx]
        subroutine_lut = {'argument': 0, 'local': 0}
        if token == 'method':
            subroutine_lut['argument'] = 1
            subroutine_lut['this'] = [self.__name, 'argument']
        token_idx += 1  # function return type
        token_idx += 1
        func_name = tokens[token_idx]
        token_idx += 1
        token = tokens[token_idx]
        # add params
        while token != ')':
            if token in ['(', ',']:
                pass
            else:
                token_idx += 1
                type = tokens[token_idx]
                self.__lut[type] = [token, 'argument', subroutine_lut['argument']]
                subroutine_lut['argument'] += 1
            token_idx += 1
            token = tokens[token_idx]
        token_idx += 1  # '{'
        token_idx += 1
        token = tokens[token_idx]
        # var
        while token == 'var':
            kind = 'local'
            token_idx += 1
            type = tokens[token_idx]
            token_idx += 1
            token = tokens[token_idx]
            while token != ';':
                if token == ',':
                    pass
                else:
                    self.__lut[token] = [type, kind, subroutine_lut[kind]]
                    subroutine_lut[kind] += 1
                token_idx += 1
                token = tokens[token_idx]
            token_idx += 1
            token = tokens[token_idx]
        self.__writer.write_func_dec(self.__name, func_name, subroutine_lut['local'])
        if func_type == 'method':
            self.__writer.write_method()
        elif func_type == 'constructor':
            self.__writer.write_constructor(self.__lut['field'][0])
        # statements
        self.statements(func_type)
        token_idx+=1

    def do_statement(self):
        global token_idx
        token_idx += 1
        token = tokens[token_idx]
        token_idx+=1
        self.call(token)
        self.__writer.write_pop('temp', 0)
        token_idx+=1

    def let_statement(self):
        global token_idx
        token_idx+=1
        var_name = tokens[token_idx]
        token_idx+=1
        token = tokens[token_idx]
        token_idx+=1
        self.expression_block()
        if token == '[':
            self.__writer.write_push(self.__lut[var_name][1], self.__lut[var_name][2])
            self.__writer.write_operation('add')
            token_idx+=1  # skip ]
            token_idx+=1  # skip =
            self.expression_block()
            self.__writer.write_pop('temp', 0)
            self.__writer.write_pop('pointer', 1)
            self.__writer.write_push('temp', 0)
            self.__writer.write_pop('that', 0)
        else:
            self.__writer.write_pop(self.__lut[var_name][1], self.__lut[var_name][2])
        token_idx+=1

    def while_statement(self, func_type):
        global token_idx
        while_name = self.__name + '.' + str(self.__lut['labels'][0])
        self.__lut['labels'][0] += 1
        token_idx+=1
        token_idx+=1
        self.__writer.write_start_label(while_name)
        self.expression_block()
        self.__writer.write_operation('not')
        self.__writer.write_if_goto(while_name + '.end')
        token_idx+=1
        token_idx+=1  # inside while
        self.statements(func_type)
        self.__writer.write_goto(while_name + '.start')
        self.__writer.write_end_label(while_name)
        token_idx+=1

    def if_statement(self, func_type):
        global token_idx
        if_name = self.__name + '.' + str(self.__lut['labels'][0])
        self.__lut['labels'][0] += 1
        token_idx+=1
        token_idx+=1  # skip '('
        self.expression_block()
        self.__writer.write_if_goto(if_name + '.iftrue')
        self.__writer.write_goto(if_name + '.iffalse')
        self.__writer.write_label(if_name + '.iftrue')
        token_idx+=1
        token_idx+=1
        self.statements(func_type)
        token_idx += 1
        token = tokens[token_idx]
        if token == 'else':
            self.__writer.write_goto(if_name + '.afterif')
            self.__writer.write_label(if_name + '.iffalse')
            token_idx+=1
            token_idx+=1
            self.statements(func_type)
            self.__writer.write_label(if_name + '.afterif')
            token_idx+=1
        else:
            self.__writer.write_label(if_name + '.iffalse')

    def return_statemtent(self, func_type):
        global token_idx
        token_idx += 1
        token = tokens[token_idx]
        if func_type == 'constructor':
            self.__writer.write_push('pointer', 0)
            self.__writer.write_return()
            token_idx+=1
            token_idx+=1
            return
        if token != ';':
            self.expression_block()
        else:
            self.__writer.write_push('constant', 0)
        self.__writer.write_return()
        token_idx+=1

    def statements(self, func_type):

        while tokens[token_idx] in ['let', 'do', 'return', 'if', 'while']:
            if tokens[token_idx] == 'let':
                self.let_statement()
            if tokens[token_idx] == 'do':
                self.do_statement()
            if tokens[token_idx] == 'return':
                self.return_statemtent(func_type)
            if tokens[token_idx] == 'if':
                self.if_statement(func_type)
            if tokens[token_idx] == 'while':
                self.while_statement(func_type)

    def call(self, func_name):
        global token_idx
        num_of_arguments = 0
        token = tokens[token_idx]
        if token == '.':
            if func_name in self.__lut:
                self.__writer.write_push(self.__lut[func_name][1],
                                         self.__lut[func_name][2])
                num_of_arguments += 1
                func_name = self.__lut[func_name][0]
            token_idx += 1
            token = tokens[token_idx]
            func_name += "." + token
            token_idx+=1
        else:
            self.__writer.write_push("pointer", 0)
            num_of_arguments += 1
            func_name = self.__name + "." + func_name
        token_idx+=1
        num_of_arguments += self.expression_list()
        self.__writer.write_call(func_name, num_of_arguments)
        token_idx+=1

    def term_block(self):
        global token_idx
        token = tokens[token_idx]
        if token.isdigit():
            self.__writer.write_push("constant", token)
            token_idx+=1
        elif token in keyword_list:
            if token == "this":
                self.__writer.write_push("pointer", 0)
            else:
                self.__writer.write_push("constant", 0)
                if token == "true":
                    self.__writer.write_operation("not")
            token_idx+=1
        elif token.startswith('"'):
            stripped_token = token[1:]
            self.__writer.write_push("constant", len(stripped_token))
            self.__writer.write_call("String.new", 1)
            for char in stripped_token:
                self.__writer.write_push("constant", ord(char))
                self.__writer.write_call("String.appendChar", 2)
            token_idx+=1
        elif not token.startswith('"') and not token.isdigit() and token not in symbol_list:
            var_name = token
            token_idx += 1
            token = tokens[token_idx]
            if token == '[':
                token_idx+=1
                self.__writer.write_push(self.__lut[var_name][1],
                                         self.__lut[var_name][2])
                self.expression_block()
                self.__writer.write_operation("add")
                token_idx+=1
                self.__writer.write_array()
            elif token == "." or token == "(":
                self.call(var_name)
            else:
                self.__writer.write_push(self.__lut[var_name][1],
                                         self.__lut[var_name][2])
        else:
            if token == "(":
                token_idx+=1
                self.expression_block()
                token_idx+=1
            elif token in ['-', '~']:
                token_idx+=1
                self.expression_block()
                if token == '-':
                    self.__writer.write_operation('neg')
                else:
                    self.__writer.write_operation('not')

    def expression_list(self):
        global token_idx
        number_of_expressions = 0
        token = tokens[token_idx]
        if token != ")":
            self.expression_block()
            number_of_expressions += 1
            token = tokens[token_idx]
            while token == ",":
                token_idx+=1
                self.expression_block()
                number_of_expressions += 1
                token = tokens[token_idx]
        return number_of_expressions

    def expression_block(self):
        global token_idx
        self.term_block()
        token = tokens[token_idx]
        while token in operations:
            token_idx+=1
            self.term_block()
            self.__writer.write_operation(operations[token])
            token = tokens[token_idx]

    def class_variables(self):
        global token_idx
        kind = tokens[token_idx]
        token_idx += 1
        type = tokens[token_idx]
        token_idx += 1
        token = tokens[token_idx]
        while token != ';':
            if token == ',':
                pass
            else:
                self.__lut[token] = [type, kind, self.__lut[kind][0]]
                self.__lut[kind][0] += 1
            token_idx += 1
            token = tokens[token_idx]
        token_idx+=1


def comments_checker(lines_before_comments_removal):
    big_comment_index = lines_before_comments_removal.find("/*")
    comment_index = lines_before_comments_removal.find("//")
    string_constant = lines_before_comments_removal.find('"')
    drop_line = lines_before_comments_removal.find("\n")
    biggest_index = len(lines_before_comments_removal) + 1
    if comment_index == -1:
        comment_index = biggest_index
    if big_comment_index == -1:
        big_comment_index = biggest_index
    if string_constant == -1:
        string_constant = biggest_index
    if comment_index > drop_line and string_constant > drop_line and drop_line < big_comment_index:
        parse_line(lines_before_comments_removal.split('\n', 1)[0])
        if len(lines_before_comments_removal.split('\n', 1)) > 1:
            comments_checker(lines_before_comments_removal.split('\n', 1)[1])
    elif comment_index > string_constant and string_constant < big_comment_index:
        parse_line(lines_before_comments_removal.split('"', 2)[0])
        tokens.append('"' + lines_before_comments_removal.split('"', 2)[1])
        comments_checker(lines_before_comments_removal.split('"', 2)[2])
    elif big_comment_index < comment_index and string_constant > big_comment_index:
        parse_line(lines_before_comments_removal.split("/*", 1)[0])
        comments_checker(lines_before_comments_removal.split("/*", 1)[1].split("*/", 1)[1])
    elif comment_index < big_comment_index and comment_index < string_constant:
        parse_line(lines_before_comments_removal.split("//", 1)[0])
        comments_checker(lines_before_comments_removal.split("\n", 1)[1])

def parse_line(line):
    global tokens
    line = line.replace('\n', "")
    line = line.replace('\t', "")
    stripped_line = line.strip()
    if not stripped_line:
        return ""
    line = line.replace(" ", "PARTITION") # this is so I could split all the tokens by having just one seperator
    for unit in line:
        if unit in symbol_list:
           line = line.replace(unit,"PARTITION" + unit + "PARTITION")
    line = line.split("PARTITION")
    for maybe_token in line:
        if maybe_token != "":
            tokens.append(maybe_token)


def parse_file(text_file, outputfile):
    global tokens
    tokens = []
    before_tokens = ""
    outputfile.seek(0)  # rereading
    for line in text_file:
        line = line.strip()
        if line:
            before_tokens += line + "\n"
    comments_checker(before_tokens)
    p = parser(outputfile, tokens)
    p.compile_class()


token_idx = 0
tokens = []


def main():
    file_name = sys.argv[1]
    if os.path.isdir(file_name):
        files = os.listdir(file_name)
        for file in files:
            if file.endswith('.jack'):
                file = os.path.join(file_name, file)
                outputfile = file[:file.index('.')] + '.vm'
                with open(file, 'r') as open_input, open(outputfile, 'w') as outputfile:
                    parse_file(open_input, outputfile)
    else:
        with open(file_name, 'r') as open_input, open(file_name[:file_name.index('.')] + '.vm', 'w') as outputfile:
            parse_file(open_input, outputfile)


if __name__ == '__main__':
    main()
