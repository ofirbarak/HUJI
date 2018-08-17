#######################################
# FILE : calculate_mathematical_expression.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: calculate operation between 2 numbers
#######################################

def calculate_mathematical_expression(num1, num2, operation):
    """
    Calculate operation between 2 numbers
    :param num1: number 1
    :param num2: number 2
    :param operation: can be one from {'*','/','+','-'}
    :return: value of (number1 [operation] number2), None - divide 0,
    iligal operation
    """
    if(operation == '/' and num2 != 0):
        return num1 / num2
    elif(operation == '*'):
        return num1 * num2
    elif(operation == '+'):
        return num1 + num2
    elif(operation == '-'):
        return num1 - num2
    else:
        return None

def calculate_from_string(op_string):
    """
    Calculate value between 2 numbers from a string
    :param op_string: string that contains '[number1] [operation] [number2]'
    :return: float value of the string
    """
    split_string = str.split(op_string, ' ')
    return calculate_mathematical_expression(float(split_string[0]),
                        float(split_string[2]), split_string[1])


print(calculate_from_string('5 - 2'))