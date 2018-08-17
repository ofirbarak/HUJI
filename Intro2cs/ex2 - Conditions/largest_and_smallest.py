#######################################
# FILE : largest_and_smallest.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: Largest and smallest numbers between 3 numbers
#######################################

def largest_between_2_numbers(num1, num2):
    """
    Help function - returns the largest number between 2 numbers
    """
    if(num1 > num2):
        return num1
    return num2

def smallest_between_2_numbers(num1, num2):
    """
    Help function - returns the smallest number between 2 numbers
    """
    if(num1 < num2):
        return num1
    return num2

def largest_and_smallest(num1, num2, num3):
    """
    Returns the smallest and largest numbers between 3 numbers,
    using the two funcrions above
    :param num1: number 1
    :param num2: number 2
    :param num3: number 3
    :return: ([largest number],[smallest number])
    """
    min_number = num1 # Start value
    # max_number = largest number between num1, num2
    max_number = largest_between_2_numbers(num1, num2)
    # Check if num1 is largest,
    # if yes--> num2 is the smallest between (num1, num2),
    #                           insert num2 to min_number
    # else(=no)--> num1 is the smallest between (num1, num2),
    #           min_number already contain num1, nothing to do
    if(max_number == num1):
        min_number = num2
    # max_number = largest number between ((num1,num2),num3)
    max_number = largest_between_2_numbers(max_number, num3)
    # min_number = smallest number between ((num1,num2),num3)
    min_number = smallest_between_2_numbers(min_number, num3)
    return max_number, min_number

