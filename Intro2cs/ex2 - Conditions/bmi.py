#######################################
# FILE : bmi.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: Check intelligent magician
#######################################

def is_normal_bmi(spells_per_hour, length_wand):
    """
    Check if is intelligent magician (=BMI - spells per hour/wand^2)
    :param spells_per_hour: Number of spells per hour
    :param length_wand: Length of wasd
    :return: True/False - True if  18.5<=BMI<=24.9
                          False otherwise
    """
    if(length_wand > 0):
        bmi = spells_per_hour / (length_wand**2)
        if(bmi >=18.5 and bmi <= 24.9):
            return True
    return False

