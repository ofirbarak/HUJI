#######################################
# FILE : shapes.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex2 2015-2016
# DESCRIPTION: Calculation of few shapes using inputs
#######################################
import math

def shape_area():
    """
    Calculate area of a chozen shape [1=circle, 2=rectangle, 3=trapezoid]
    :return: The calculate area
    """
    area_type = int(input("Choose shape (1=circle, 2=rectangle, 3=trapezoid): "))
    calc_area = None # Define area to None

    if(area_type == 1):
        # Getting input for radius and calculate the area
        radius = float(input())
        calc_area = return_area_of_circle(radius)

    elif(area_type == 2):
        # Getting input for 2 edges and calculate the area
        a_edge = float(input())
        b_edge = float(input())
        calc_area = return_area_of_rectangle(a_edge, b_edge)

    elif(area_type == 3):
        # Getting input for 2 edges, height and calculate the area
        a_edge = float(input())
        b_edge = float(input())
        height = float(input())
        calc_area = return_area_of_trapezoid(a_edge, b_edge, height)
    else:
        # No area to be calculated
        None
    return calc_area

def return_area_of_circle(radius):
    """
    Calculate area of circle = pi*r^2
    :param radius: radius of circle
    :return: Area of circle
    """
    return math.pi * radius**2

def return_area_of_rectangle(a_edge, b_edge):
    """
    Calculate area of rectangle = a*b
    :param a_side: One edge
    :param b_side: Seconed edge
    :param height: Height
    :return: Area of rectangle
    """
    return a_edge * b_edge

def return_area_of_trapezoid(a_edge, b_edge, height):
    """
    Calculate area of trapezoid = ((a+b)/2) * h
    :param a_edge: One edge
    :param b_edge: Seconed edge
    :param height: Height
    :return: Area of trapezoid
    """
    return ((a_edge+b_edge)/2) * height


