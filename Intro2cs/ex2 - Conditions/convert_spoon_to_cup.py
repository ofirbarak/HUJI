#######################################
# FILE : convert_spoon_to_cup.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: calculate number of spoons in cup
#######################################

# Constants
SPOONS_IN_CUPS = 3.5 # The number of spoons in cups


def convert_spoon_to_cup(spoons):
    """
    :param spoons: number of spoons
    :return: number of spoons in cups
    """
    cups = spoons / SPOONS_IN_CUPS
    return cups
