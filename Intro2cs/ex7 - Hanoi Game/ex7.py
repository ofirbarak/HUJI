#######################################
# FILE : ex7.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex7 2015-2016
# DESCRIPTION: Recursion
#######################################
# Constants
ZERO = 0
ONE = 1
TWO = 2
EMPTY_LIST = []
EMPTY_STRING = ''
ZERO_STRING = '0'
ONE_STRING = '1'

# Functions
def print_to_n(n):
    '''
    Gets a number and prints all numbers from 1 to n
    '''
    if n >= ONE:
        print_to_n(n-ONE)
        print(n)


def print_reversed_n(n):
    '''
    print all numbers from n to 1
    '''
    if n > ZERO:
        print(n)
        if n == ONE:
            return
        return print_reversed_n(n-ONE)


def is_prime(n):
    '''
    Check if n is prime
    '''
    if n == ONE:
        return False
    if n < ONE or n%ONE != ZERO:
        return False
    return has_divisor_smaller_than(n, (n-ONE)//TWO + ONE)


def has_divisor_smaller_than(n, i):
    '''
    Help functoion - check if there is smaller divisor
    '''
    if i == ZERO:
        return True
    if i == ONE or n%i != ZERO:
        return has_divisor_smaller_than(n, i-ONE)
    return False


def divisors(n):
    '''
    Returns a list of all integers that divided by n
    '''
    if n == ZERO:
        return EMPTY_LIST
    return get_list_divisors(abs(n), abs(n))


def get_list_divisors(n, i):
    '''
    Returns a list of all integers that divided by n,
        assuming that 1<=i<n
    '''
    if i == ONE:
        return [ONE]
    if n%i == ZERO:
        return get_list_divisors(n, i - ONE) + [i]
    return get_list_divisors(n, i-ONE)


def exp_n_x(n, x):
    '''
    Return sum exponent function of n
    '''
    if n == ZERO:
        return ONE
    return x**n/get_factorial_n(n) + exp_n_x(n-ONE, x)


def get_factorial_n(n):
    '''
    Help function - Get n factorial
    '''
    if n == ONE or n == ZERO:
        return ONE
    return n * get_factorial_n(n-ONE)


def play_hanoi(hanoi, n, src, dest, temp):
    '''
    Playing hanoi game
    '''
    if n >= ONE:
        play_hanoi(hanoi, n-ONE, src, temp, dest)
        hanoi.move(src, dest)
        play_hanoi(hanoi, n-ONE, temp, dest, src)


def print_binary_sequences(n):
    '''
    Print all matches 0,1 in length n
    '''
    print_binary_sequences_with_prefix('', n)


def print_binary_sequences_with_prefix(prefix, n):
    '''
    Print all possible sequences starts wirh a prefix
    '''
    if n == ZERO:
        print(prefix)
    if n > ZERO:
        print_binary_sequences_with_prefix(prefix+ZERO_STRING, n-ONE)
        print_binary_sequences_with_prefix(prefix+ONE_STRING, n-ONE)


def print_sequences(char_list, n):
    '''
    Print all sequences of char list in length n
    '''
    change_seq(char_list, n, EMPTY_STRING, ZERO)


def change_seq(char_list, n, seq_list, index):
    '''
    Print sequences in length n from char list with a prefix
    '''
    if n == ZERO:
        return print(seq_list)
    if n > ZERO:
        for char in char_list:
            change_seq(char_list, n-ONE, seq_list+char, ZERO)


def print_no_repetition_sequences(char_list, n):
    '''
    Print sequences without repetetion
    '''
    print_no_repetition_with_prefix(char_list, n, EMPTY_STRING, ZERO)


def print_no_repetition_with_prefix(char_list, n, prefix, index):
    '''
    Print sequences with a prefix without repetition
    '''
    if index == len(char_list):
        index = ZERO
    if n == ZERO:
        return print(EMPTY_STRING.join(prefix))
    if char_list[index] not in list(prefix):
        print_no_repetition_with_prefix(char_list, n-ONE,
                                        prefix + char_list[index],
                                        index)
    # Check the combines for each prefix
    while index+1 < len(char_list):
        if char_list[index+1] not in list(prefix):
            print_no_repetition_with_prefix(char_list, n-ONE,
                                            prefix + char_list[index+ONE],
                                            ZERO)
        index += ONE


def no_repetition_sequences_list(char_list, n):
    '''
    Return list of not repetetion in length n
    '''
    if n == ZERO:
        return [EMPTY_STRING]
    return get_no_repetition_with_prefix(char_list, n, EMPTY_STRING,
                                         ZERO, EMPTY_LIST)


def get_no_repetition_with_prefix(char_list, n, prefix, index, ret_list):
    if index == len(char_list):
        index = ZERO
    if n == ZERO:
        # Update the list
        return ret_list.append(prefix)
    # Check if we can add that number to prefix (have to be different)
    if char_list[index] not in list(prefix):
        get_no_repetition_with_prefix(char_list, n-ONE,
                                      prefix + char_list[index],
                                      index, ret_list)
    while index+ONE < len(char_list):
        if char_list[index+ONE] not in list(prefix):
            get_no_repetition_with_prefix(char_list, n-ONE,
                                          prefix + char_list[index+ONE],
                                          ZERO, ret_list)
        index += ONE
    return ret_list


