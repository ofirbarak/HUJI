#######################################
# FILE : ex3.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex3 2015-2016
# DESCRIPTION: Loop exercises
#######################################

def create_list():
    """
    Gets inputs, put them in a list
    :return: List of inputs
    """
    inputs = []
    str_element = input()
    while str_element != '':
        inputs.append(str_element)
        str_element = input()

    return inputs

def concat_list(lst_str):
    """
    Connenct all strings
    :param lst_str:  List of strings
    :return: Concatenation of the list
    """
    full_string = ''
    for str_part in lst_str:
        full_string += str_part

    return full_string

def avr(num_list):
    """
    Calculate the average
    :param num_list: List of float numbers
    :return: Average of all numbers in the list
    """
    # Check if there is numbers in list, if not return None
    if len(num_list) == 0:
        return None

    sum_list = 0
    for number in num_list:
        sum_list += number

    return sum_list/len(num_list)

def cyclic(lst1, lst2):
    """
    Check if two list are circular shift
    :param lst1: One list of numbers
    :param lst2: Other list of numbers
    :return: True if they are, otherwise return False
    """
    # Check if two lists are in same length, if not return False
    if len(lst1) != len(lst2):
        return False
    # Length of lst2. (Done because of high use)
    len2 = len(lst2)
    # If both are empty, return True.
    if len2 == 0:
        return True
    # Find the index in lst2 of first object in lst1
    indent = lst2.index(lst1[0])
    # Compare each object in lst1 to lst2 with acoording to the indention
    for index1 in range(len2):
        if not is_same_object(lst1[index1], lst2[(index1+indent)%len2]):
            return False

    return True

def is_same_object(obj1, obj2):
    """
    Chaeck if two object are the same
    :param obj1: Object 1
    :param obj2: Object 2
    :return: True if yes, False otherwise
    """
    if obj1 == obj2:
        return True
    return False

def hist(n, list_num):
    """
    Histogramia - number of times that each item from range numbers
        appears in a given number
    :param n: Number n
    :param list_num: Range of numbers
    :return: List in legth n, that indicate how much time the index of the
        cell appears in the given number
    """
    indicator = list()
    indicator = [0] * n
    for number in list_num:
        indicator[number] += 1
    return indicator

def fact(n):
    """
    Factorization
    :param n: Positive integer n
    :return: List from decomposition of a number
    """
    primers = list()
    for index in range(2, n):
        # Check if we arrived to end
        if n == 1:
            break
        # Check if index is a divisor of n
        # If yes, move forward in checks
        if n%index == 0:
            #Another loop - to check if index is a primer
            is_primery = True
            for index_secondary in range(2, index):
                # If index_secondary is a divisor of index,
                #       index is not primer, brake the cycle of the upper loop
                if (index % index_secondary) == 0:
                    is_primery = False
                    break
            # Is index is a primer? If yes, add it to list (=primers)
            #   and divide n as much as we can without a remainder
            if is_primery:
                while n % index == 0:
                    primers.append(index)
                    n = n / index

    return primers

def cart(lst1,lst2):
    """
    Cartesian product
    :param lst1: List 1
    :param lst2: List 2
    :return: List contains Lists of pairs arranged
    """
    pairs_arranged = list()
    # If at least one list empty, skip the loop and return empty list
    if not(len(lst1) == 0 or len(lst2) == 0):
        # Loop for each list, to generate the pair
        for item1 in lst1:
            for item2 in lst2:
                pairs_arranged.append([item1, item2])

    return pairs_arranged

def pair(n, num_list):
    """
    Pairs equals sum
    :param n: Positive integer n
    :param num_list: Integer list
    :return: pairs that sum equals to n
    """
    pairs_sum = list()
    """
    The algorithm is:
    Given: n , num_list=[ <a1>, <a2>, <a3>, <a4>, ..., <an> ]
    The checks are as follows:
    <a1> + <a2> =? n
    <a1> + <a3> =? n
    .
    .
    .
    <a1> + <an> =? n
    then,
    <a2> + <a3> =? n
    <a2> + <a4> =? n
    .
    .
    .
    <a(n-1)> + <an> =? n
    """
    for index1 in range(len(num_list)-1):
        for index2 in range(index1,len(num_list)):
            item1 = num_list[index1]
            item2 = num_list[index2]
            if item1 + item2 == n:
                pairs_sum.append([item1, item2])

    # Check if there are pair, if not return None
    if(len(pairs_sum) == 0):
        return None
    return pairs_sum

