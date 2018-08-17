#######################################
# FILE : largest_and_smallest.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: Solution for quadratic equation
#######################################

def quadratic_equation(a, b,c):
    """
    Calculate the solutions for quadratic equation
    :param a: Coefficient of X^2
    :param b: Coefficient of X
    :param c: Coefficient of free variable
    :return: Solution
    """
    # Define solutions to default
    solution1 = None
    solution2 = None

    if(a == 0):
        # There is no quadratic equation => No solutions, already defined
        # Pass to end (return the solutions)
        None

    else:
        delta = return_delta(a, b, c)
        """
        Delta > 0 --> 2 solutions
        Delta = 0 --> 1 solution
        Delta < 0 --> no solutions
        """
        if(delta < 0):
            solution1 = None
            solution2 = None
        elif(delta == 0):
            solution1 = (-1*b) / (2*a)
            solution2 = None
        else:
            # Solution[1,2] = (-b [+/-] square(Delta)) / (2a)
            squrt_Delta = delta**0.5
            solution1 = (-1*b + squrt_Delta) / (2*a)
            solution2 = (-1*b - squrt_Delta) / (2*a)
    return solution1, solution2

def return_delta(a, b, c):
    """
    Check the Delta to find how much solutions will be
    Delta = b^2 - 4*a*c
    :param a: Coefficient of X^2
    :param b: Coefficient of X
    :param c: Coefficient of free variable
    :return: Delta
    """
    delta = b**2 - 4*a*c
    return delta

def quadratic_equation_user_input():
    a, b, c = input("Insert coefficients a,b, and c: ").split(' ')
    solution1, solution2 = quadratic_equation(int(a), int(b), int(c))
    if(solution1 == None and solution2 == None):
        print("The equation has no solutions.")
    elif(solution1 != None and solution2 == None):
        print("The equation has 1 solution:", solution1)
    else:
        print("The equation has 2 solutions:", solution1,"and", solution2)

