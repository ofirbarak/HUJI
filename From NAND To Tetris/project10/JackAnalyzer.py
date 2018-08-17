import sys
import os

keyword_list = ['class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void',
                'true', 'false', 'null', 'this', 'let', 'do', 'if',
                'else', 'while', 'return']
symbol_list = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
               '-', '*', '/', '&', '|', '<', '>', '=', '~']
special_symbol = ['<=', '>=', '!=', '++', '--']


def parse_class(outputfile):
    global token_idx
    outputfile.write("<class>\n")
    outputfile.write("<keyword>" + "class" + "</keyword>\n")
    outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    while tokens[token_idx] in ["static", "field"]:
        variables("classVarDec", outputfile)
    while tokens[token_idx] in ["constructor", "function", "method"]:
        function_declare(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    outputfile.write("</class>\n")

def variables(str, outputfile):
    global token_idx
    outputfile.write("<" + str + ">" + "\n")
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    if tokens[token_idx] in keyword_list:
        outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    if tokens[token_idx] not in keyword_list:
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    while tokens[token_idx] == ",":
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
        token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    outputfile.write("</" + str + ">\n")

def function_declare(outputfile):
    global token_idx
    outputfile.write("<subroutineDec>\n")
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    if tokens[token_idx] in keyword_list:
        outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    if tokens[token_idx] not in keyword_list:
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    function_variable_list(outputfile)
    function_body(outputfile)
    outputfile.write("</subroutineDec>\n")

def function_variable_list(outputfile):
    global token_idx
    outputfile.write("<parameterList>\n")
    while tokens[token_idx] != ")":
        outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
        token_idx += 1
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
        token_idx += 1
        if tokens[token_idx] == ",":
            outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
            token_idx += 1
    outputfile.write("</parameterList>\n")
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1

def function_body(outputfile):
    global token_idx
    outputfile.write("<subroutineBody>\n")
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    while tokens[token_idx] == "var":
        variables("varDec", outputfile)
    statements(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    outputfile.write("</subroutineBody>\n")

def statements(outputfile):
    global token_idx
    outputfile.write("<statements>\n")
    while tokens[token_idx] in ["do", "if", "let", "while", "return"]:
        if tokens[token_idx] == "do":
            outputfile.write("<doStatement>\n")
            do_statement(outputfile)
            outputfile.write("</doStatement>\n")
        elif tokens[token_idx] == "let":
            outputfile.write("<letStatement>\n")
            let_statement(outputfile)
            outputfile.write("</letStatement>\n")
        elif tokens[token_idx] == "if":
            outputfile.write("<ifStatement>\n")
            if_statement(outputfile)
            outputfile.write("</ifStatement>\n")
        elif tokens[token_idx] == "while":
            outputfile.write("<whileStatement>\n")
            while_statement(outputfile)
            outputfile.write("</whileStatement>\n")
        elif tokens[token_idx] == "return":
            outputfile.write("<returnStatement>\n")
            return_statement(outputfile)
            outputfile.write("</returnStatement>\n")
    outputfile.write("</statements>\n")

def let_statement(outputfile):
    global token_idx
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    if tokens[token_idx] == "[":
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
        expression_block(outputfile)
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    expression_block(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1

def do_statement(outputfile):
    global token_idx
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    token_idx += 1
    function_call(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1


def function_call(outputfile):
    global token_idx
    if tokens[token_idx] == ".":
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
        token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    expression_list_block(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1

def while_statement(outputfile):
    global token_idx
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    expression_block(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    statements(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1

def if_statement(outputfile):
    global token_idx
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    expression_block(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    statements(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1
    if tokens[token_idx] == "else":
        outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
        token_idx += 1
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
        statements(outputfile)
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1

def return_statement(outputfile):
    global token_idx
    outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
    token_idx += 1
    if tokens[token_idx] != ";":
        expression_block(outputfile)
    outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
    token_idx += 1


def expression_list_block(outputfile):
    global token_idx
    outputfile.write("<expressionList>\n")
    if tokens[token_idx] != ")":
        expression_block(outputfile)
        while tokens[token_idx] == ",":
            outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
            token_idx += 1
            expression_block(outputfile)
    outputfile.write("</expressionList>\n")

def expression_block(outputfile):
    global token_idx
    outputfile.write("<expression>\n")
    term_block(outputfile)
    while tokens[token_idx] in ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']:
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
        term_block(outputfile)
    outputfile.write("</expression>\n")

def term_block(outputfile):
    global token_idx
    outputfile.write("<term>\n")
    flag = False
    if tokens[token_idx].isdigit():
        flag = True
        outputfile.write("<integerConstant>" + tokens[token_idx] + "</integerConstant>\n")
    if tokens[token_idx] in keyword_list:
        outputfile.write("<keyword>" + tokens[token_idx] + "</keyword>\n")
        flag = True
    if tokens[token_idx].startswith('"'):
        flag = True
        outputfile.write("<stringConstant>" + tokens[token_idx][1:] + "</stringConstant>\n")
    if tokens[token_idx] in symbol_list or tokens[token_idx] in ['&amp;','&lt;','&gt;']:
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        flag = True
    if not flag:
        outputfile.write("<identifier>" + tokens[token_idx] + "</identifier>\n")
    if tokens[token_idx] == "(":
        token_idx += 1
        expression_block(outputfile)
        outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
        token_idx += 1
    elif tokens[token_idx] in ["-", "~"]:
        token_idx += 1
        term_block(outputfile)
    else:
        token_idx += 1
        if tokens[token_idx] == "[":
            outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
            token_idx += 1
            expression_block(outputfile)
            outputfile.write("<symbol>" + tokens[token_idx] + "</symbol>\n")
            token_idx += 1
        if tokens[token_idx] in [".", "("]:
            function_call(outputfile)
    outputfile.write("</term>\n")



def match_appended_token_to_xml_type_style(str):
    if str == "&":
        return "&amp;"
    if str == ">":
        return "&gt;"
    if str == "<":
        return "&lt;"
    return str

def check_comments(line, i):
    ger = line.find('"')
    comment_index = line.find('//')
    start_cmt = line.find('/*')
    end_cmt = line.find('*/')
    if comment_index != -1:
        if (ger != -1 and comment_index < ger) or ger == -1:
            line = line[:comment_index]
    if start_cmt != -1 and end_cmt != -1:
        line = line[:start_cmt] + line[end_cmt+2:]
        i = 0
    elif start_cmt == -1 and end_cmt != -1:
        line = line[end_cmt+2:]
        i = 0
    elif start_cmt != -1 and end_cmt == -1:
        line = ''
        i = 0
    return line, i

def parse_line(line):
    flag = False
    if line.startswith('*'):
        return []
    tokens = list()
    str = ''
    i = 0
    while i < len(line):
        comment_index = line.find('//')
        start_cmt = line.find('/*')
        ger = line.find('"')
        if ger != -1 and (start_cmt != -1 and ger > start_cmt) or (comment_index != -1 and ger > comment_index):
            line,i = check_comments(line, i)
        elif ger == -1:
            line, i = check_comments(line, i)

        if len(line) == 0:
            return tokens
        s = line[i]
        str += s
        if s == ' ':
            str = ''
            i += 1
        elif s == '"':
            i += 1
            while i < len(line) and line[i] != '"':
                s = line[i]
                str += s
                i += 1
            i += 1
            tokens.append(match_appended_token_to_xml_type_style(str))
            str = ''
        elif i + 1 < len(line) and (line[i + 1] == ' ' or line[i + 1] in symbol_list):
            tokens.append(match_appended_token_to_xml_type_style(str))
            str = ''
            i += 1
        elif s in symbol_list:
            if not (i + 1 < len(line) and line[i + 1] in symbol_list):
                if str in special_symbol:
                    tokens.append(match_appended_token_to_xml_type_style(str))
                else:
                    for j in str:
                        tokens.append(match_appended_token_to_xml_type_style(j))
                str = ''
                i += 1
        else:
            i += 1
    return tokens




def parse_file(open_input, outputfile):
    global tokens
    tokens = []
    global token_idx
    token_idx = 1
    with open(open_input, 'r') as text_file:
        for line in text_file:
            line = line.strip()
            ret = parse_line(line)
            if ret != []:
                tokens += ret
        parse_class(outputfile)


token_idx = 1
tokens = []
def main():
    filename = sys.argv[1]
    if os.path.isdir(filename):
        for file in os.listdir(filename):
            if file.endswith(".jack"):
                output = os.path.join(filename, file[:file.index('.')] + ".xml")
                with open(output, 'w') as outputfile:
                    parse_file(os.path.join(filename, file), outputfile)
    if filename.endswith(".jack"):
        output = filename[:filename.index('.')] + ".xml"
        with open(output, 'w') as outputfile:
            parse_file(filename, outputfile)

if __name__ == "__main__":
    main()